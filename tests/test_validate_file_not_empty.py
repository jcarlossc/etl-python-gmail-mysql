from pathlib import Path

from etl_python_gmail_mysql.validation.validate_file_not_empty import (
    get_validate_file_not_empty,
)


def test_validate_file_not_empty_com_conteudo(
    tmp_path: Path,
) -> None:
    """Deve retornar True quando o arquivo possuir conteúdo."""

    # Cria um arquivo temporário com conteúdo.
    file_path = tmp_path / "vendas.csv"
    file_path.write_text("produto,quantidade\nPizza,10")

    result = get_validate_file_not_empty(file_path)

    assert result is True


def test_validate_file_not_empty_arquivo_vazio(
    tmp_path: Path,
) -> None:
    """Deve retornar False quando o arquivo estiver vazio."""

    # Cria um arquivo temporário vazio.
    file_path = tmp_path / "vendas.csv"
    file_path.touch()

    result = get_validate_file_not_empty(file_path)

    assert result is False


def test_validate_file_not_empty_arquivo_inexistente(
    tmp_path: Path,
) -> None:
    """Deve retornar False quando o arquivo não existir."""

    file_path = tmp_path / "vendas.csv"

    result = get_validate_file_not_empty(file_path)

    assert result is False
