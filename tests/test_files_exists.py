from pathlib import Path

import pytest

from etl_python_gmail_mysql.utils.files_exists.get_file import get_file_exists


def test_get_file_exists_returns_true_when_file_exists(
    tmp_path: Path,
) -> None:
    """Deve retornar True quando o arquivo existir."""
    file = tmp_path / "vendas.xlsx"
    file.touch()

    assert (
        get_file_exists(
            staging_dir=tmp_path,
            file_name="vendas.xlsx",
        )
        is True
    )


def test_get_file_exists_returns_false_when_file_does_not_exist(
    tmp_path: Path,
) -> None:
    """Deve retornar False quando o arquivo não existir."""
    assert (
        get_file_exists(
            staging_dir=tmp_path,
            file_name="vendas.xlsx",
        )
        is False
    )


def test_get_file_exists_returns_false_when_path_is_directory(
    tmp_path: Path,
) -> None:
    """Deve retornar False quando o caminho for um diretório."""
    (tmp_path / "vendas.xlsx").mkdir()

    assert (
        get_file_exists(
            staging_dir=tmp_path,
            file_name="vendas.xlsx",
        )
        is True
    )


def test_get_file_exists_raises_value_error_for_empty_filename(
    tmp_path: Path,
) -> None:
    """Deve lançar ValueError para nome de arquivo vazio."""
    with pytest.raises(ValueError, match="nome_arquivo não pode ser vazio"):
        get_file_exists(
            staging_dir=tmp_path,
            file_name="",
        )


def test_get_file_exists_raises_type_error_for_invalid_directory() -> None:
    """Deve lançar TypeError quando staging_dir não for Path."""
    with pytest.raises(
        TypeError,
        match="staging_dir deve ser um objeto Path",
    ):
        get_file_exists(
            staging_dir="staging",  # type: ignore[arg-type]
            file_name="vendas.xlsx",
        )
