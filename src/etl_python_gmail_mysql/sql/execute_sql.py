import logging
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def execute_sql(
    engine: Engine,
    sql_file: Path,
) -> None:
    """Executa os comandos de um arquivo SQL.

    A função lê o arquivo SQL, separa os comandos
    utilizando ponto e vírgula e executa cada instrução
    sequencialmente dentro de uma única transação SQLAlchemy.

    Args: engine:
        Engine utilizada para conexão com o banco de dados.
        sql_file: Caminho do arquivo SQL.

    Raises: FileNotFoundError: Se o arquivo SQL não existir.
        ValueError: Se o arquivo SQL não possuir comandos.
        RuntimeError: Se ocorrer erro durante a execução do script SQL.

    """

    logger = logging.getLogger(__name__)

    logger.info("Executando script SQL: %s", sql_file)

    try:
        # Lê o conteúdo do arquivo SQL.
        sql = sql_file.read_text(encoding="utf-8")

        # Separa os comandos SQL utilizando ';'.
        statements = [
            statement.strip() for statement in sql.split(";") if statement.strip()
        ]

        if not statements:
            raise ValueError(f"Arquivo SQL vazio ou sem comandos: {sql_file}")

        # Executa todos os comandos dentro de uma única transação.
        with engine.begin() as connection:
            for statement in statements:
                logger.debug("Executando comando SQL.")
                connection.execute(text(statement))

        logger.info("Script SQL executado com sucesso.")

    except FileNotFoundError:
        logger.error(
            "Arquivo SQL não encontrado: %s",
            sql_file,
        )
        raise

    except ValueError:
        logger.error(
            "Arquivo SQL vazio ou inválido: %s",
            sql_file,
        )
        raise

    except SQLAlchemyError as error:
        logger.exception("Erro ao executar script SQL.")

        raise RuntimeError("Erro ao executar script SQL.") from error
