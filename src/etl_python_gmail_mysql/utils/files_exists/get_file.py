from pathlib import Path


def get_file_exists(
    staging_dir: Path,
    file_name: str,
) -> bool:
    """
    Verifica se um arquivo recebido já existe no diretório de staging.

    A função é utilizada para evitar o processamento duplicado de
    arquivos recebidos pela aplicação.

    Args:
        staging_dir: Diretório onde os arquivos recebidos são armazenados.
        nome_arquivo: Nome do arquivo que será verificado.

    Returns:
        True se o arquivo existir no diretório de staging.
        False caso o arquivo não exista.

    Raises:
        TypeError: Se staging_dir não for um objeto Path.
        ValueError: Se o nome do arquivo estiver vazio.
        OSError: Se ocorrer um erro ao acessar o sistema de arquivos.
    """

    try:
        # Valida o tipo do diretório recebido.
        if not isinstance(staging_dir, Path):
            raise TypeError("staging_dir deve ser um objeto Path.")

        # Evita verificar um caminho sem nome de arquivo.
        if not file_name:
            raise ValueError("nome_arquivo não pode ser vazio.")

        # Monta o caminho completo do arquivo.
        path_dir = staging_dir / file_name

        # exists() garante que o caminho aponta para um arquivo
        # e para um diretório existente.
        return path_dir.exists()

    except (TypeError, ValueError):
        # Mantém os erros de validação para que o chamador
        # possa identificar o problema nos argumentos.
        raise

    except OSError as error:
        # Converte erros do sistema de arquivos em uma mensagem
        # mais clara para o contexto da aplicação.
        raise OSError(
            f"FILE_ERROR: erro ao verificar o arquivo '{file_name}': {error}"
        ) from error
