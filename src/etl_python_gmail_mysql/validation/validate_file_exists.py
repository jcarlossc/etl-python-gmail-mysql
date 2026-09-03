from pathlib import Path


def get_validate_file_exists(
    file_path: Path,
) -> bool:
    try:
        if not isinstance(file_path, Path):
            raise TypeError("file_path deve ser uma instância de Path.")

        return file_path.exists() and file_path.is_file()

    except OSError:
        return False
