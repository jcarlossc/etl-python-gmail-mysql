import pandas as pd
import pytest

from etl_python_gmail_mysql.standardization.validate_types import (
    get_validate_types,
)


@pytest.fixture
def columns_config() -> dict[str, dict[str, str]]:
    """Configuração de tipos utilizada nos testes."""
    return {
        "sales_types": {
            "id_venda": "Int64",
            "id_cliente": "Int64",
            "produto": "string",
            "quantidade": "Int64",
            "preco_unitario": "float64",
            "total": "float64",
            "data_venda": "datetime64[ns]",
        },
        "customer_types": {
            "id_cliente": "Int64",
            "nome": "string",
            "email": "string",
            "cidade": "string",
            "estado": "string",
        },
    }


def test_get_validate_types_sales(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Testa a conversão dos tipos do DataFrame de vendas."""

    df = pd.DataFrame(
        {
            "id_venda": ["1", "2"],
            "id_cliente": ["10", "20"],
            "produto": [100, 200],
            "quantidade": ["2", "3"],
            "preco_unitario": ["10.50", "20.00"],
            "total": ["21.00", "60.00"],
            "data_venda": [
                "2026-01-01",
                "2026-01-02",
            ],
        }
    )

    result = get_validate_types(df, columns_config)

    assert result["id_venda"].dtype == "Int64"
    assert result["id_cliente"].dtype == "Int64"
    assert result["produto"].dtype == "string"
    assert result["quantidade"].dtype == "Int64"
    assert result["preco_unitario"].dtype == "float64"
    assert result["total"].dtype == "float64"

    assert pd.api.types.is_datetime64_dtype(result["data_venda"])


def test_get_validate_types_customer(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Testa a conversão dos tipos do DataFrame de clientes."""

    df = pd.DataFrame(
        {
            "id_cliente": ["1", "2"],
            "nome": [100, 200],
            "email": [300, 400],
            "cidade": [500, 600],
            "estado": [700, 800],
        }
    )

    result = get_validate_types(df, columns_config)

    assert result["id_cliente"].dtype == "Int64"
    assert result["nome"].dtype == "string"
    assert result["email"].dtype == "string"
    assert result["cidade"].dtype == "string"
    assert result["estado"].dtype == "string"


def test_get_validate_types_does_not_modify_original(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Verifica se o DataFrame original permanece inalterado."""

    df = pd.DataFrame(
        {
            "id_venda": ["1", "2"],
            "quantidade": ["2", "3"],
        }
    )

    original = df.copy()

    result = get_validate_types(df, columns_config)

    # O resultado deve ser diferente do DataFrame original.
    assert result["id_venda"].dtype == "Int64"

    # O DataFrame original deve continuar com os valores originais.
    pd.testing.assert_frame_equal(df, original)


def test_get_validate_types_ignores_missing_columns(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Verifica se colunas ausentes são simplesmente ignoradas."""

    df = pd.DataFrame(
        {
            "id_venda": ["1", "2"],
            "produto": ["Produto A", "Produto B"],
        }
    )

    result = get_validate_types(df, columns_config)

    assert result["id_venda"].dtype == "Int64"
    assert result["produto"].dtype == "string"

    # A função não deve criar colunas ausentes.
    assert "quantidade" not in result.columns
    assert "total" not in result.columns


def test_get_validate_types_invalid_date(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Verifica se uma data inválida gera ValueError."""

    df = pd.DataFrame(
        {
            "data_venda": [
                "2026-01-01",
                "data_invalida",
            ]
        }
    )

    with pytest.raises(
        ValueError,
        match="Não foi possível converter",
    ):
        get_validate_types(df, columns_config)


def test_get_validate_types_invalid_integer(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Verifica se um valor inválido para inteiro gera ValueError."""

    df = pd.DataFrame(
        {
            "id_venda": [
                "1",
                "abc",
            ]
        }
    )

    with pytest.raises(
        ValueError,
        match="Não foi possível converter",
    ):
        get_validate_types(df, columns_config)


def test_get_validate_types_invalid_dataframe(
    columns_config: dict[str, dict[str, str]],
) -> None:
    """Verifica se a função rejeita entrada que não seja DataFrame."""

    with pytest.raises(
        TypeError,
        match="O argumento df deve ser um pandas DataFrame",
    ):
        get_validate_types(
            ["1", "2"],
            columns_config,
        )
