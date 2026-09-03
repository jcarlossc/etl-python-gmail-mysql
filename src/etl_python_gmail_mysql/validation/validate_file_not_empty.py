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

    logger.info("Iniciando validação de arquivo não vazio")

    try:
        # Obtém o tamanho do arquivo em bytes.
        return file_path.stat().st_size > 0

    except FileNotFoundError:
        # Arquivo inexistente é considerado inválido.
        logger.warning("Arquivo não encontrado: %s", file_path)
        return False

    except OSError as exc:
        # Trata outros erros relacionados ao sistema de arquivos.
        logger.error(
            "Erro ao acessar o arquivo %s: %s",
            file_path,
            exc,
        )
        return False
