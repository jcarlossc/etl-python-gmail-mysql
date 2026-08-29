from pathlib import Path


def get_file_exists(
    staging_dir: Path,
    file_name: str,
) -> bool:
    try:
        if not isinstance(staging_dir, Path):
            raise TypeError("staging_dir deve ser um objeto Path.")

        if not file_name:
            raise ValueError("nome_arquivo não pode ser vazio.")

        path_dir = staging_dir / file_name

        return path_dir.is_file()

    except (TypeError, ValueError):
        raise

    except OSError as error:
        raise OSError(
            f"FILE_ERROR: erro ao verificar o arquivo '{file_name}': {error}"
        ) from error
