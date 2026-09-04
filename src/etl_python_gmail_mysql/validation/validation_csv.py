from pathlib import Path

import pandas as pd

from etl_python_gmail_mysql.validation.validate_file_exists import (
    get_validate_file_exists,
)
from etl_python_gmail_mysql.validation.validate_file_extension import (
    get_validate_file_extension,
)
from etl_python_gmail_mysql.validation.validate_file_not_empty import (
    get_validate_file_not_empty,
)


def get_validate_csv(
    file_path: Path,
) -> pd.DataFrame:
    """
    Valida e carrega um arquivo CSV.

    Args:
        file_path: Caminho do arquivo CSV.

    Returns:
        DataFrame contendo os dados do CSV.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se a extensão não for suportada,
            o arquivo estiver vazio ou ocorrer erro na leitura.
    """

    # Valida se o arquivo existe.
    if not get_validate_file_exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Valida se o arquivo possui extensão CSV.
    if not get_validate_file_extension(file_path):
        raise ValueError(f"Extensão não suportada: {file_path.suffix}")

    # Impede o processamento de arquivos vazios.
    if not get_validate_file_not_empty(file_path):
        raise ValueError(f"Arquivo vazio: {file_path.name}")

    try:
        # Carrega o conteúdo do CSV em um DataFrame.
        df = pd.read_csv(file_path)

    except Exception as exc:
        # Converte erros do pandas para uma exceção da aplicação.
        raise ValueError(f"Erro ao ler o CSV: {file_path.name}") from exc

    return df
