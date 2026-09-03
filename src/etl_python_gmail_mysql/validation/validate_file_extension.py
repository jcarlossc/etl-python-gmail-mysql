import logging
from pathlib import Path


def validate_file_extension(
    file_path: Path,
) -> bool:
    """
    Verifica se a extensão do arquivo é suportada pelo pipeline.

    Args:
        file_path: Caminho do arquivo que será validado.

    Returns:
        True se a extensão for CSV ou XLSX, caso contrário False.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando validação de extensão")

    # Extensões aceitas pelo pipeline de processamento.
    allowed_extensions = {
        ".csv",
        ".xlsx",
    }

    # Normaliza a extensão para letras minúsculas antes da comparação.
    return file_path.suffix.lower() in allowed_extensions
