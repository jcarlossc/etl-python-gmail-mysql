from pathlib import Path

import pytest

from etl_python_gmail_mysql.utils.clean.clean_name import get_clean_name


def test_get_clean_name_clientes() -> None:
    """Testa a extração do nome lógico de um arquivo de clientes."""

    file_path = Path("2026_08_26_17_04_05_clientes_janeiro.xlsx")

    result = get_clean_name(file_path)

    assert result == "clientes_janeiro"


def test_get_clean_name_vendas() -> None:
    """Testa a extração do nome lógico de um arquivo de vendas."""

    file_path = Path("2026_08_26_17_04_05_vendas_janeiro.csv")

    result = get_clean_name(file_path)

    assert result == "vendas_janeiro"


def test_get_clean_name_fevereiro() -> None:
    """Testa a extração do tipo e período para fevereiro."""

    file_path = Path("2026_08_27_09_30_10_clientes_fevereiro.xlsx")

    result = get_clean_name(file_path)

    assert result == "clientes_fevereiro"


def test_get_clean_name_returns_string() -> None:
    """Testa se a função retorna uma string."""

    file_path = Path("2026_08_26_17_04_05_vendas_janeiro.csv")

    result = get_clean_name(file_path)

    assert isinstance(result, str)


def test_get_clean_name_invalid_filename() -> None:
    """Testa erro para nomes de arquivo inválidos."""

    file_path = Path("clientes.xlsx")

    with pytest.raises(
        ValueError,
        match="Nome de arquivo inválido",
    ):
        get_clean_name(file_path)
