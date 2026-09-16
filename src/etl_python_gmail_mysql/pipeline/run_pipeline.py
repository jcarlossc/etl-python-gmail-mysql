import logging
from pathlib import Path

import pandas as pd
from googleapiclient.errors import HttpError
from sqlalchemy.exc import SQLAlchemyError

from etl_python_gmail_mysql.cleanning.clean_data import get_clean_dataframe
from etl_python_gmail_mysql.database.connection_db import get_engine
from etl_python_gmail_mysql.integration.integrate_sales_clients import (
    get_integrate_sales_clients,
)
from etl_python_gmail_mysql.schema.create_star_schema import get_create_star_schema
from etl_python_gmail_mysql.services.gmail.attachments import save_attachments
from etl_python_gmail_mysql.services.gmail.authentication import get_gmail_service
from etl_python_gmail_mysql.services.gmail.labels import get_label_id
from etl_python_gmail_mysql.services.gmail.messages import get_messages
from etl_python_gmail_mysql.services.retry import retry
from etl_python_gmail_mysql.sql.execute_sql import get_execute_sql
from etl_python_gmail_mysql.staging.get_staging import move_to_staging
from etl_python_gmail_mysql.standardization.validate_types import get_validate_types
from etl_python_gmail_mysql.utils.clean.clean_name import get_clean_name
from etl_python_gmail_mysql.utils.loggers.logger import setup_logger
from etl_python_gmail_mysql.utils.settings.Settings import Settings
from etl_python_gmail_mysql.utils.yaml.get_yaml import load_all_configs
from etl_python_gmail_mysql.validation.validation_csv import get_validation_csv
from etl_python_gmail_mysql.validation.validation_xlsx import get_validation_xlsx


logger = logging.getLogger(__name__)


def get_run_pipeline() -> None:
    """
    Executa o pipeline completo de ETL.

    O pipeline realiza as seguintes etapas:

    1. Carregamento das configurações.
    2. Configuração do logging.
    3. Autenticação na API do Gmail.
    4. Download dos anexos.
    5. Movimentação dos arquivos para staging.
    6. Validação, conversão e limpeza dos dados.
    7. Integração entre vendas e clientes.
    8. Criação do Star Schema.
    9. Execução do script SQL.
    10. Encerramento da conexão com o banco.

    Raises:
        RuntimeError: Se ocorrer um erro durante a execução do pipeline.
    """
    engine = None

    try:
        # ---------------------------------------------------------
        # 1. Configurações
        # ---------------------------------------------------------
        config_path = Path("config")

        configs = load_all_configs(config_path)

        setup_logger(configs["logging"])

        logger.info("Iniciando pipeline ETL.")

        settings = Settings()

        logger.info("Settings carregadas.")

        # ---------------------------------------------------------
        # 2. Diretórios
        # ---------------------------------------------------------
        download_dir = Path("data/downloads")
        staging_dir = Path("data/stagings")

        base_dir = Path(__file__).resolve().parents[3]

        # ---------------------------------------------------------
        # 3. Configuração do Gmail
        # ---------------------------------------------------------
        scopes = [configs["gmail"]["gmail"]["scopes"]]

        credentials_file = base_dir / configs["gmail"]["gmail"]["credentials"]

        token_file = base_dir / configs["gmail"]["gmail"]["token"]

        # ---------------------------------------------------------
        # 4. Autenticação Gmail
        # ---------------------------------------------------------
        service = retry(
            func=lambda: get_gmail_service(
                scopes=scopes,
                base_dir=base_dir,
                credentials_file=credentials_file,
                token_file=token_file,
            ),
            exceptions=(HttpError,),
            max_attempts=3,
            delay=1.0,
        )

        logger.info("Autenticação Gmail concluída.")

        # ---------------------------------------------------------
        # 5. Mensagens e anexos
        # ---------------------------------------------------------
        label_id = get_label_id(
            service,
            "EMPRESA/01_ENTRADA",
        )

        messages = get_messages(
            service,
            label_id,
        )

        logger.info(
            "Mensagens encontradas: %d",
            len(messages),
        )

        for message in messages:
            message_id = message["id"]

            save_attachments(
                service,
                message_id,
                download_dir,
            )

        logger.info("Download dos anexos concluído.")

        # ---------------------------------------------------------
        # 6. Staging
        # ---------------------------------------------------------
        result = move_to_staging(
            download_dir=download_dir,
            staging_dir=staging_dir,
        )

        logger.info(
            "CSV movidos para staging: %s",
            result["csv"],
        )

        logger.info(
            "XLSX movidos para staging: %s",
            result["xlsx"],
        )

        csv_dir = staging_dir / "csv"
        xlsx_dir = staging_dir / "xlsx"

        # ---------------------------------------------------------
        # 7. Validação e transformação
        # ---------------------------------------------------------
        clientes: dict[str, pd.DataFrame] = {}
        vendas: dict[str, pd.DataFrame] = {}

        # CSV - vendas
        for file_path in csv_dir.glob("*.csv"):
            df_csv = get_validation_csv(file_path)

            logger.info(
                "CSV validado: %s",
                file_path.name,
            )

            df_csv_types = get_validate_types(
                df_csv,
                configs["columns_types"],
            )

            logger.info(
                "Tipos do CSV validados: %s",
                file_path.name,
            )

            df_csv_clean = get_clean_dataframe(df_csv_types)

            logger.info(
                "Limpeza concluída: %s",
                file_path.name,
            )

            data_type = get_clean_name(file_path)

            if data_type.startswith("vendas_"):
                periodo = data_type.removeprefix("vendas_")

                vendas[periodo] = df_csv_clean

        # XLSX - clientes
        for file_path in xlsx_dir.glob("*.xlsx"):
            df_xlsx = get_validation_xlsx(file_path)

            logger.info(
                "XLSX validado: %s",
                file_path.name,
            )

            df_xlsx_types = get_validate_types(
                df_xlsx,
                configs["columns_types"],
            )

            logger.info(
                "Tipos do XLSX validados: %s",
                file_path.name,
            )

            df_xlsx_clean = get_clean_dataframe(df_xlsx_types)

            logger.info(
                "Limpeza concluída: %s",
                file_path.name,
            )

            data_type = get_clean_name(file_path)

            if data_type.startswith("clientes_"):
                periodo = data_type.removeprefix("clientes_")

                clientes[periodo] = df_xlsx_clean

        # ---------------------------------------------------------
        # 8. Integração vendas + clientes
        # ---------------------------------------------------------
        dados_integrados: list[pd.DataFrame] = []

        for periodo in sorted(vendas):
            if periodo not in clientes:
                logger.warning(
                    "Não existe arquivo de clientes para o período: %s",
                    periodo,
                )
                continue

            df_integrated = get_integrate_sales_clients(
                df_sales=vendas[periodo],
                df_clients=clientes[periodo],
            )

            dados_integrados.append(df_integrated)

            logger.info(
                "Integração concluída: %s",
                periodo,
            )

        if not dados_integrados:
            raise RuntimeError("Nenhum período válido foi integrado.")

        # Junta todos os períodos.
        df_integrado = pd.concat(
            dados_integrados,
            ignore_index=True,
        )

        logger.info(
            "Dados integrados: %d registros.",
            len(df_integrado),
        )

        # ---------------------------------------------------------
        # 9. Star Schema
        # ---------------------------------------------------------
        star_schema = get_create_star_schema(
            df_integrated=df_integrado,
        )

        logger.info(
            "Star Schema criado: %s",
            list(star_schema.keys()),
        )

        # ---------------------------------------------------------
        # 10. Banco de dados
        # ---------------------------------------------------------
        engine = retry(
            func=lambda: get_engine(settings),
            exceptions=(SQLAlchemyError,),
            max_attempts=3,
            delay=1.0,
        )

        sql_file = (
            Path(__file__).resolve().parents[1] / "sql" / "create_sales_database.sql"
        )

        get_execute_sql(
            engine,
            sql_file,
        )

        logger.info("Script SQL executado com sucesso.")

        logger.info("Pipeline ETL concluído com sucesso.")

    except (HttpError, SQLAlchemyError, OSError, ValueError) as error:
        logger.exception("Erro durante a execução do pipeline.")

        raise RuntimeError("Falha na execução do pipeline ETL.") from error

    finally:
        # Garante que a conexão seja encerrada mesmo
        # quando ocorrer uma exceção.
        if engine is not None:
            engine.dispose()

            logger.info("Conexão com o banco encerrada.")
