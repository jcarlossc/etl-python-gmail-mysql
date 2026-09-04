from pathlib import Path

import pandas as pd
from etl_python_gmail_mysql.validation.validation_file_exists import (
    get_validate_file_exists,
)
from etl_python_gmail_mysql.validation.validation_file_extension import (
    get_validate_file_extension,
)
from etl_python_gmail_mysql.validation.validation_file_not_empty import (
    get_validate_file_not_empty,
)


def validate_csv(
    file_path: Path,
) -> pd.DataFrame:
    if not get_validate_file_exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    if not get_validate_file_extension(file_path):
        raise ValueError(f"Extensão não suportada: {file_path.suffix}")

    if not get_validate_file_not_empty(file_path):
        raise ValueError(f"Arquivo vazio: {file_path.name}")

    try:
        df = pd.read_csv(file_path)

    except Exception as exc:
        raise ValueError(f"Erro ao ler o CSV: {file_path.name}") from exc

    return df
