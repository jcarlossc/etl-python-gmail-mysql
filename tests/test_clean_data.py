import pandas as pd
import pytest

from etl_python_gmail_mysql.cleanning.clean_data import (
    get_clean_dataframe,
)


def test_clean_dataframe_removes_duplicates() -> None:
    """Testa a remoção de registros duplicados."""

    df = pd.DataFrame(
        {
            "id_venda": [1, 1, 2],
            "produto": ["Notebook", "Notebook", "Mouse"],
            "quantidade": [1, 1, 2],
            "preco_unitario": [1000.0, 1000.0, 50.0],
            "total": [1000.0, 1000.0, 100.0],
        }
    )

    result = get_clean_dataframe(df)

    assert len(result) == 2


def test_clean_dataframe_removes_spaces() -> None:
    """Testa a remoção de espaços dos campos textuais."""

    df = pd.DataFrame(
        {
            "produto": ["  Notebook  ", " Mouse "],
        }
    )

    result = get_clean_dataframe(df)

    assert result.loc[0, "produto"] == "Notebook"
    assert result.loc[1, "produto"] == "Mouse"


def test_clean_dataframe_removes_invalid_quantity() -> None:
    """Testa a remoção de quantidades menores ou iguais a zero."""

    df = pd.DataFrame(
        {
            "quantidade": [2, 0, -1, 3],
        }
    )

    result = get_clean_dataframe(df)

    assert result["quantidade"].tolist() == [2, 3]


def test_clean_dataframe_removes_negative_price() -> None:
    """Testa a remoção de preços negativos."""

    df = pd.DataFrame(
        {
            "preco_unitario": [100.0, -50.0, 200.0],
        }
    )

    result = get_clean_dataframe(df)

    assert result["preco_unitario"].tolist() == [
        100.0,
        200.0,
    ]


def test_clean_dataframe_removes_negative_total() -> None:
    """Testa a remoção de totais negativos."""

    df = pd.DataFrame(
        {
            "total": [100.0, -20.0, 300.0],
        }
    )

    result = get_clean_dataframe(df)

    assert result["total"].tolist() == [
        100.0,
        300.0,
    ]


def test_clean_dataframe_does_not_modify_original() -> None:
    """Testa se o DataFrame original permanece inalterado."""

    df = pd.DataFrame(
        {
            "produto": ["  Notebook  "],
        }
    )

    original = df.copy()

    get_clean_dataframe(df)

    pd.testing.assert_frame_equal(df, original)


def test_clean_dataframe_rejects_non_dataframe() -> None:
    """Testa erro quando o argumento não é um DataFrame."""

    with pytest.raises(TypeError):
        get_clean_dataframe(["Notebook", "Mouse"])


def test_clean_dataframe_rejects_empty_dataframe() -> None:
    """Testa erro para DataFrame vazio."""

    df = pd.DataFrame()

    with pytest.raises(ValueError):
        get_clean_dataframe(df)


def test_clean_dataframe_converts_invalid_date_to_nat() -> None:
    """Testa o tratamento de datas inválidas."""

    df = pd.DataFrame(
        {
            "data_venda": [
                "2026-01-01",
                "data inválida",
            ],
        }
    )

    result = get_clean_dataframe(df)

    assert result.loc[0, "data_venda"] == pd.Timestamp("2026-01-01")

    assert pd.isna(result.loc[1, "data_venda"])
