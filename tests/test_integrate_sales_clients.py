import pandas as pd
import pytest

from etl_python_gmail_mysql.integration.integrate_sales_clients import (
    get_integrate_sales_clients,
)


def test_get_integrate_sales_clients() -> None:
    """Testa a integração entre vendas e clientes."""

    df_sales = pd.DataFrame(
        {
            "id_venda": [1, 2, 3],
            "id_cliente": [10, 20, 10],
            "produto": ["Mouse", "Teclado", "Monitor"],
        }
    )

    df_clients = pd.DataFrame(
        {
            "id_cliente": [10, 20],
            "nome": ["Carlos", "João"],
            "cidade": ["Recife", "Olinda"],
        }
    )

    result = get_integrate_sales_clients(
        df_sales=df_sales,
        df_clients=df_clients,
    )

    assert len(result) == 3
    assert "nome" in result.columns
    assert "cidade" in result.columns

    assert result.loc[0, "nome"] == "Carlos"
    assert result.loc[1, "nome"] == "João"
    assert result.loc[2, "nome"] == "Carlos"


def test_get_integrate_sales_clients_preserves_sales() -> None:
    """Testa se todas as vendas são preservadas."""

    df_sales = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "id_cliente": [10, 20],
        }
    )

    df_clients = pd.DataFrame(
        {
            "id_cliente": [10, 20],
            "nome": ["Carlos", "João"],
        }
    )

    result = get_integrate_sales_clients(
        df_sales=df_sales,
        df_clients=df_clients,
    )

    assert result["id_venda"].tolist() == [1, 2]


def test_get_integrate_sales_clients_unknown_client() -> None:
    """Testa venda cujo cliente não existe na dimensão de clientes."""

    df_sales = pd.DataFrame(
        {
            "id_venda": [1, 2],
            "id_cliente": [10, 99],
        }
    )

    df_clients = pd.DataFrame(
        {
            "id_cliente": [10],
            "nome": ["Carlos"],
        }
    )

    result = get_integrate_sales_clients(
        df_sales=df_sales,
        df_clients=df_clients,
    )

    # A venda deve ser preservada pelo left join.
    assert len(result) == 2

    assert result.loc[0, "nome"] == "Carlos"
    assert pd.isna(result.loc[1, "nome"])


def test_get_integrate_sales_clients_duplicate_client() -> None:
    """Testa erro quando existe cliente duplicado."""

    df_sales = pd.DataFrame(
        {
            "id_venda": [1],
            "id_cliente": [10],
        }
    )

    df_clients = pd.DataFrame(
        {
            "id_cliente": [10, 10],
            "nome": ["Carlos", "João"],
        }
    )

    with pytest.raises(RuntimeError, match="Erro ao integrar vendas e clientes"):
        get_integrate_sales_clients(
            df_sales=df_sales,
            df_clients=df_clients,
        )


def test_get_integrate_sales_clients_missing_column() -> None:
    """Testa erro quando a chave de integração não existe."""

    df_sales = pd.DataFrame(
        {
            "id_venda": [1],
            "id_cliente": [10],
        }
    )

    df_clients = pd.DataFrame(
        {
            "cliente": [10],
            "nome": ["Carlos"],
        }
    )

    with pytest.raises(RuntimeError, match="Erro ao integrar vendas e clientes"):
        get_integrate_sales_clients(
            df_sales=df_sales,
            df_clients=df_clients,
        )
