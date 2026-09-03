from pathlib import Path

from etl_python_gmail_mysql.validation.validate_file_extension import (
    get_validate_file_extension,
)


def test_validate_file_extension_csv() -> None:
    """Deve retornar True para arquivos CSV."""

    file_path = Path("vendas.csv")

    result = get_validate_file_extension(file_path)

    assert result is True


def test_validate_file_extension_xlsx() -> None:
    """Deve retornar True para arquivos XLSX."""

    file_path = Path("vendas.xlsx")

    result = get_validate_file_extension(file_path)

    assert result is True


def test_validate_file_extension_csv_maiusculo() -> None:
    """Deve aceitar extensão CSV em letras maiúsculas."""

    file_path = Path("vendas.CSV")

    result = get_validate_file_extension(file_path)

    assert result is True


def test_validate_file_extension_xlsx_maiusculo() -> None:
    """Deve aceitar extensão XLSX em letras maiúsculas."""

    file_path = Path("vendas.XLSX")

    result = get_validate_file_extension(file_path)

    assert result is True


def test_validate_file_extension_extensao_nao_suportada() -> None:
    """Deve retornar False para extensões não suportadas."""

    file_path = Path("vendas.pdf")

    result = get_validate_file_extension(file_path)

    assert result is False


def test_validate_file_extension_sem_extensao() -> None:
    """Deve retornar False quando o arquivo não possuir extensão."""

    file_path = Path("vendas")

    result = get_validate_file_extension(file_path)

    assert result is False
