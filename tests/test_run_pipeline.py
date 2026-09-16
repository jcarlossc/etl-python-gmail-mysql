from pathlib import Path

import pandas as pd

import etl_python_gmail_mysql.pipeline.run_pipeline as pipeline


def test_get_run_pipeline_success(monkeypatch):
    """
    Testa a execução bem-sucedida do pipeline completo.

    Todas as dependências externas são simuladas para testar apenas
    a orquestração realizada por get_run_pipeline().
    """

    configs = {
        "logging": {},
        "gmail": {
            "gmail": {
                "scopes": ["scope"],
                "credentials": "credentials.json",
                "token": "token.json",
            }
        },
        "columns_types": {},
    }

    class FakeEngine:
        def __init__(self):
            self.disposed = False

        def dispose(self):
            self.disposed = True

    fake_engine = FakeEngine()

    # Arquivos simulados
    sales_file = Path("vendas_janeiro.csv")
    clients_file = Path("clientes_janeiro.xlsx")

    # Configurações
    monkeypatch.setattr(
        pipeline,
        "load_all_configs",
        lambda _: configs,
    )

    monkeypatch.setattr(
        pipeline,
        "setup_logger",
        lambda _: None,
    )

    monkeypatch.setattr(
        pipeline,
        "Settings",
        lambda: object(),
    )

    # Gmail
    monkeypatch.setattr(
        pipeline,
        "get_gmail_service",
        lambda **kwargs: object(),
    )

    monkeypatch.setattr(
        pipeline,
        "get_label_id",
        lambda service, label: "label-id",
    )

    monkeypatch.setattr(
        pipeline,
        "get_messages",
        lambda service, label_id: [],
    )

    monkeypatch.setattr(
        pipeline,
        "save_attachments",
        lambda service, message_id, download_dir: None,
    )

    # Staging
    monkeypatch.setattr(
        pipeline,
        "move_to_staging",
        lambda download_dir, staging_dir: {
            "csv": [sales_file],
            "xlsx": [clients_file],
        },
    )

    # Arquivos encontrados no staging
    def fake_glob(self, pattern):
        if pattern == "*.csv":
            return [sales_file]

        if pattern == "*.xlsx":
            return [clients_file]

        return []

    monkeypatch.setattr(
        pipeline.Path,
        "glob",
        fake_glob,
    )

    # DataFrames simulados
    sales_df = pd.DataFrame(
        {
            "id_cliente": [1],
            "produto": ["Produto A"],
            "quantidade": [2],
        }
    )

    clients_df = pd.DataFrame(
        {
            "id_cliente": [1],
            "nome": ["Cliente A"],
        }
    )

    monkeypatch.setattr(
        pipeline,
        "get_validation_csv",
        lambda path: sales_df,
    )

    monkeypatch.setattr(
        pipeline,
        "get_validation_xlsx",
        lambda path: clients_df,
    )

    monkeypatch.setattr(
        pipeline,
        "get_validate_types",
        lambda df, types: df,
    )

    monkeypatch.setattr(
        pipeline,
        "get_clean_dataframe",
        lambda df: df,
    )

    # Identificação do período
    def fake_clean_name(path):
        if path.suffix == ".csv":
            return "vendas_janeiro"

        return "clientes_janeiro"

    monkeypatch.setattr(
        pipeline,
        "get_clean_name",
        fake_clean_name,
    )

    # Integração
    integrated_df = pd.DataFrame(
        {
            "id_cliente": [1],
            "produto": ["Produto A"],
            "nome": ["Cliente A"],
        }
    )

    monkeypatch.setattr(
        pipeline,
        "get_integrate_sales_clients",
        lambda df_sales, df_clients: integrated_df,
    )

    # Star schema
    monkeypatch.setattr(
        pipeline,
        "get_create_star_schema",
        lambda df_integrated: {"dim_cliente": integrated_df},
    )

    # Banco
    monkeypatch.setattr(
        pipeline,
        "get_engine",
        lambda settings: fake_engine,
    )

    monkeypatch.setattr(
        pipeline,
        "get_execute_sql",
        lambda engine, sql_file: None,
    )

    # Executa retry imediatamente
    monkeypatch.setattr(
        pipeline,
        "retry",
        lambda func, **kwargs: func(),
    )

    # Executa o pipeline
    pipeline.get_run_pipeline()

    # Verifica se a conexão foi encerrada
    assert fake_engine.disposed is True
