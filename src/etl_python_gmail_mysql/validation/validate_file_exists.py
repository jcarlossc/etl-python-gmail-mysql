from pathlib import Path


def get_validate_file_exists(
    file_path: Path,
) -> bool:
    """
    Verifica se o caminho informado corresponde a um arquivo existente.

    Args:
        file_path: Caminho do arquivo que será validado.

    Returns:
        True se o arquivo existir, caso contrário False.

    Raises:
        TypeError: Se file_path não for uma instância de Path.
    """

    try:
        # Garante que o parâmetro recebido seja um objeto Path.
        if not isinstance(file_path, Path):
            raise TypeError("file_path deve ser uma instância de Path.")

        # Verifica se o caminho existe e se corresponde a um arquivo.
        return file_path.exists() and file_path.is_file()

    except OSError:
        # Erros relacionados ao sistema de arquivos são tratados
        # como arquivo não disponível.
        return False
