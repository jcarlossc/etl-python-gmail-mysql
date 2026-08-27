import re


def sanitize_filename(filename: str) -> str:

    sanitized = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        filename,
    ).strip()

    return sanitized