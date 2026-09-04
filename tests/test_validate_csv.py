import pandas as pd
import pytest

from etl_python_gmail_mysql.validation.validation_csv import get_validation_csv


def test_validate_csv_com_dados_validos(tmp_path):
    """Deve carregar um CSV válido em um DataFrame."""
    file_path = tmp_path / "vendas.csv"

    file_path.write_text(
        "produto,quantidade\nNotebook,2\nMouse,5\n",
        encoding="utf-8",
    )

    df = get_validation_csv(file_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["produto", "quantidade"]


def test_validate_csv_arquivo_nao_existe(tmp_path):
    """Deve lançar FileNotFoundError para arquivo inexistente."""
    file_path = tmp_path / "vendas.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Arquivo não encontrado",
    ):
        get_validation_csv(file_path)


def test_validate_csv_extensao_invalida(tmp_path):
    """Deve rejeitar arquivos que não sejam CSV."""
    file_path = tmp_path / "vendas.txt"

    file_path.write_text(
        "produto,quantidade\nNotebook,2\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Extensão não suportada",
    ):
        get_validation_csv(file_path)


def test_validate_csv_arquivo_vazio(tmp_path):
    """Deve rejeitar arquivos CSV vazios."""
    file_path = tmp_path / "vendas.csv"

    file_path.write_text("", encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="Arquivo vazio",
    ):
        get_validation_csv(file_path)
