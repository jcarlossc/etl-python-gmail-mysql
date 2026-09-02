import logging
from pathlib import Path
import shutil


def move_to_staging(
    download_dir: Path,
    staging_dir: Path,
) -> dict[str, int]:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando remoção de arquivos para staging")

    if not download_dir.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {download_dir}")

    csv_dir = staging_dir / "csv"
    xlsx_dir = staging_dir / "xlsx"

    try:
        csv_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        xlsx_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        moved_files = {
            "csv": 0,
            "xlsx": 0,
        }

        for file_path in download_dir.iterdir():
            if not file_path.is_file():
                continue

            extension = file_path.suffix.lower()

            if extension == ".csv":
                destination = csv_dir / file_path.name

            elif extension == ".xlsx":
                destination = xlsx_dir / file_path.name

            else:
                continue

            try:
                shutil.move(
                    file_path,
                    destination,
                )

            except OSError as exc:
                logger.error(
                    "Erro ao copiar o arquivo %s para %s.",
                    file_path,
                    destination,
                )

                raise RuntimeError(
                    f"Erro ao copiar o arquivo {file_path} para {destination}."
                ) from exc

            moved_files[extension[1:]] += 1

            logger.info("Arquivos movidos para staging com sucesso")

        return moved_files

    except OSError as exc:
        logger.error(
            "Erro ao processar o diretório de staging: %s",
            staging_dir,
        )

        raise RuntimeError(
            f"Erro ao processar o diretório de staging: {staging_dir}."
        ) from exc
