import re


def sanitize_filename(filename: str) -> str:

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