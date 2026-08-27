import pytest

from etl_python_gmail_mysql.utils.sanitize.get_sanitize import sanitize_filename


@pytest.mark.parametrize(
    ("filename", "expected"),
    [
        # Caracteres inválidos individuais.
        ("arquivo<teste>.txt", "arquivo_teste_.txt"),
        ("arquivo:teste.txt", "arquivo_teste.txt"),
        ('arquivo"teste".txt', "arquivo_teste_.txt"),
        ("arquivo/teste.txt", "arquivo_teste.txt"),
        (r"arquivo\teste.txt", "arquivo_teste.txt"),
        ("arquivo|teste.txt", "arquivo_teste.txt"),
        ("arquivo?teste.txt", "arquivo_teste.txt"),
        ("arquivo*teste.txt", "arquivo_teste.txt"),
        # Vários caracteres inválidos no mesmo nome.
        (
            "Vendas: Agosto/2026 <final>?.xlsx",
            "Vendas_ Agosto_2026 _final__.xlsx",
        ),
        # Espaços nas extremidades.
        (
            "  vendas_2026.xlsx  ",
            "vendas_2026.xlsx",
        ),
        # Nome válido não deve ser alterado.
        (
            "vendas_2026.xlsx",
            "vendas_2026.xlsx",
        ),
        # Caracteres acentuados devem ser preservados.
        (
            "Relatório de Vendas.xlsx",
            "Relatório de Vendas.xlsx",
        ),
    ],
)
def test_sanitize_filename(filename: str, expected: str) -> None:
    """Deve sanitizar corretamente nomes de arquivos."""
    assert sanitize_filename(filename) == expected


def test_sanitize_filename_preserves_extension() -> None:
    """Deve preservar a extensão do arquivo."""
    result = sanitize_filename("Vendas: Agosto/2026.xlsx")

    assert result.endswith(".xlsx")


@pytest.mark.parametrize(
    "filename",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_sanitize_filename_empty_name(filename: str) -> None:
    """Deve rejeitar nomes vazios após o strip."""
    with pytest.raises(
        ValueError,
        match="filename não pode ser vazio",
    ):
        sanitize_filename(filename)


@pytest.mark.parametrize(
    "filename",
    [
        None,
        123,
        10.5,
        [],
        {},
        True,
    ],
)
def test_sanitize_filename_invalid_type(filename: object) -> None:
    """Deve rejeitar valores que não sejam strings."""
    with pytest.raises(
        TypeError,
        match="filename deve ser uma string",
    ):
        sanitize_filename(filename)  # type: ignore[arg-type]
