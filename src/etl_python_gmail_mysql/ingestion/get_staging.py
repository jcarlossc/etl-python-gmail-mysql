import logging
import shutil
from pathlib import Path


def move_to_staging(
    download_dir: Path,
    staging_dir: Path,
) -> dict[str, int]:
    """
    Move arquivos CSV e XLSX do diretório de downloads para o staging.

    Args:
        download_dir: Diretório contendo os arquivos baixados.
        staging_dir: Diretório de destino do staging.

    Returns:
        Dicionário contendo a quantidade de arquivos movidos por extensão.

    Raises:
        FileNotFoundError:
            Quando o diretório de downloads não existe.
        RuntimeError:
            Quando ocorre um erro durante o processamento dos arquivos.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando remoção de arquivos para staging")

    # Verifica se o diretório de origem existe.
    if not download_dir.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {download_dir}")

    # Define os diretórios de destino por tipo de arquivo
    csv_dir = staging_dir / "csv"
    xlsx_dir = staging_dir / "xlsx"

    try:
        # Cria os diretórios de destino.
        csv_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        xlsx_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Contadores dos arquivos copiados.
        moved_files = {
            "csv": 0,
            "xlsx": 0,
        }

        # Percorre os arquivos do diretório de downloads.
        for file_path in download_dir.iterdir():
            # Ignora diretórios e outros itens que não sejam arquivos.
            if not file_path.is_file():
                continue

            # Obtém a extensão em letras minúsculas.
            extension = file_path.suffix.lower()

            # Define o destino dos arquivos CSV.
            if extension == ".csv":
                destination = csv_dir / file_path.name

            # Define o destino dos arquivos XLSX.
            elif extension == ".xlsx":
                destination = xlsx_dir / file_path.name

            # Ignora extensões não suportadas.
            else:
                continue

            try:
                # Copia o arquivo preservando metadados.
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

            # Atualiza o contador da extensão correspondente.
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
