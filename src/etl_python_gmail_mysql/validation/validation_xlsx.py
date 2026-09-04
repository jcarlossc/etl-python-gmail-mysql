import logging
from pathlib import Path

import pandas as pd

from etl_python_gmail_mysql.validation.validate_file_exists import (
    get_validate_file_exists,
)
from etl_python_gmail_mysql.validation.validate_file_not_empty import (
    get_validate_file_not_empty,
)


def get_validation_xlsx(
    file_path: Path,
) -> pd.DataFrame:
    """
    Valida e carrega um arquivo XLSX.

    Args:
        file_path: Caminho do arquivo XLSX.

    Returns:
        DataFrame contendo os dados da planilha.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se a extensão não for suportada,
            o arquivo estiver vazio ou ocorrer erro na leitura.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando validação dos arquivos XLSX.")

    # Verifica se o arquivo existe.
    if not get_validate_file_exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    # Verifica se a extensão do arquivo é suportada.
    if file_path.suffix.lower() != ".xlsx":
        raise ValueError(f"Extensão não suportada: {file_path.suffix}")

    # Impede o processamento de arquivos vazios.
    if not get_validate_file_not_empty(file_path):
        raise ValueError(f"Arquivo vazio: {file_path.name}")

    try:
        # Carrega a planilha XLSX em um DataFrame.
        df = pd.read_excel(file_path)

    except Exception as exc:
        # Converte o erro de leitura para uma exceção da aplicação.
        raise ValueError(f"Erro ao ler o XLSX: {file_path.name}") from exc

    logger.info("Validação dos arquivos XLSX realizada com sucesso.")

    return df
