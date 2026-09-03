from pathlib import Path

from etl_python_gmail_mysql.validation.validate_file_exists import (
    get_validate_file_exists,
)


def test_validate_file_exists_arquivo_existente(tmp_path: Path) -> None:
    """Deve retornar True quando o arquivo existir."""

    # Cria um arquivo temporário para o teste.
    file_path = tmp_path / "vendas.csv"
    file_path.write_text("produto,quantidade\nPizza,10")

    # Executa a função.
    result = get_validate_file_exists(file_path)

    # Verifica o resultado esperado.
    assert result is True


def test_validate_file_exists_arquivo_inexistente(
    tmp_path: Path,
) -> None:
    """Deve retornar False quando o arquivo não existir."""

    file_path = tmp_path / "vendas.csv"

    result = get_validate_file_exists(file_path)

    assert result is False


def test_validate_file_exists_diretorio(tmp_path: Path) -> None:
    """Deve retornar False quando o caminho for um diretório."""

    directory = tmp_path / "dados"
    directory.mkdir()

    result = get_validate_file_exists(directory)

    assert result is False
