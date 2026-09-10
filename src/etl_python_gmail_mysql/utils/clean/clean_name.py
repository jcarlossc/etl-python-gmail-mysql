from pathlib import Path


def get_clean_name(file_path: Path) -> str:
    """Extrai o tipo e o período do nome do arquivo.

    Args:
        file_path: objeto Path

    Returns:
        string: Nome dos DataFrames
    """

    try:
        # Remove a extensão e separa o nome em partes.
        parts = file_path.stem.split("_")

        # O nome deve possuir:
        # 6 partes para data/hora + tipo + período.
        if len(parts) < 8:
            raise ValueError(f"Nome de arquivo inválido: {file_path.name}")

        # Remove as seis primeiras partes (data e hora)
        # e mantém o tipo e o período.
        return "_".join(parts[6:])

    except (IndexError, AttributeError) as exc:
        raise ValueError(f"Nome de arquivo inválido: {file_path.name}") from exc
