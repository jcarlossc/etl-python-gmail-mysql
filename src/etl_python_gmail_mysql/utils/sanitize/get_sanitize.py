import re


def sanitize_filename(filename: str) -> str:
    """
    Remove caracteres inválidos para nomes de arquivos.

    Caracteres inválidos são substituídos por `_` e espaços em branco
    nas extremidades do nome são removidos.

    Args:
        filename: Nome do arquivo que será sanitizado.

    Returns:
        Nome adequado para utilização no sistema de arquivos.

    Raises:
        TypeError: Se `filename` não for uma string.
        ValueError: Se o nome resultar em uma string vazia.

    Examples:
        >>> sanitize_filename("Vendas: Agosto/2026.xlsx")
        'Vendas_ Agosto_2026.xlsx'
    """

    if not isinstance(filename, str):
        raise TypeError("filename deve ser uma string.")

    sanitized = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        filename,
    ).strip()

    if not sanitized:
        raise ValueError("filename não pode ser vazio.")    

    return sanitized