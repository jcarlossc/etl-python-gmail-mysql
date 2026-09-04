import pandas as pd
import pytest

from etl_python_gmail_mysql.validation.validation_xlsx import get_validation_xlsx


def test_validate_xlsx_com_dados_validos(tmp_path):
    """Deve carregar um XLSX válido em um DataFrame."""
    file_path = tmp_path / "vendas.xlsx"

    df_original = pd.DataFrame(
        {
            "produto": ["Notebook", "Mouse"],
            "quantidade": [2, 5],
        }
    )

    df_original.to_excel(
        file_path,
        index=False,
    )

    df = get_validation_xlsx(file_path)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["produto", "quantidade"]


def test_validate_xlsx_arquivo_nao_existe(tmp_path):
    """Deve lançar FileNotFoundError para arquivo inexistente."""
    file_path = tmp_path / "vendas.xlsx"

    with pytest.raises(
        FileNotFoundError,
        match="Arquivo não encontrado",
    ):
        get_validation_xlsx(file_path)


def test_validate_xlsx_extensao_invalida(tmp_path):
    """Deve rejeitar arquivos com extensão não suportada."""
    file_path = tmp_path / "vendas.csv"

    file_path.write_text(
        "produto,quantidade\nNotebook,2\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Extensão não suportada",
    ):
        get_validation_xlsx(file_path)


def test_validate_xlsx_arquivo_vazio(tmp_path):
    """Deve rejeitar arquivos XLSX vazios."""
    file_path = tmp_path / "vendas.xlsx"

    file_path.touch()

    with pytest.raises(
        ValueError,
        match="Arquivo vazio",
    ):
        get_validation_xlsx(file_path)
