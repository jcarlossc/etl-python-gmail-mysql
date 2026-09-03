import logging
from pathlib import Path


def get_validate_file_not_empty(
    file_path: Path,
) -> bool:
    """
    Verifica se o arquivo possui conteúdo.

    Args:
        file_path: Caminho do arquivo que será validado.

    Returns:
        True se o arquivo possuir conteúdo, caso contrário False.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando validação de arquivos não vazios")

    # Obtém o tamanho do arquivo em bytes.
    return file_path.stat().st_size > 0
