from pathlib import Path


def get_clean_name(file_path: Path) -> str:
    try:
        parts = file_path.stem.split("_")

        if len(parts) < 8:
            raise ValueError(f"Nome de arquivo inválido: {file_path.name}")

        return "_".join(parts[6:])

    except (IndexError, AttributeError) as exc:
        raise ValueError(f"Nome de arquivo inválido: {file_path.name}") from exc
