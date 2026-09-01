import base64
import logging
from datetime import UTC, datetime
from pathlib import Path

from googleapiclient.discovery import Resource

from etl_python_gmail_mysql.utils.sanitize.get_sanitize import sanitize_filename


def save_attachments(
    service: Resource,
    message_id: str,
    output_dir: Path,
) -> list[str]:
    """
    Salva os anexos de uma mensagem utilizando o Subject
    como nome-base do arquivo.

    O arquivo será salvo no formato:

        YYYY_MM_DD_HH_MM_SS_subject.ext

    Exemplo:

        2026_08_21_09_34_01_vendas.xlsx

    A data e hora utilizadas são as da mensagem do Gmail,
    e não a data/hora da execução do programa. Dessa forma,
    o mesmo arquivo terá o mesmo nome em execuções futuras.

    Args:
        service: Serviço autenticado do Gmail.
        message_id: ID da mensagem.
        output_dir: Diretório de saída.

    Returns:
        Lista com os nomes dos arquivos encontrados/salvos.

    Raises:
        RuntimeError: Erro ao salvar anexos.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando download de anexos")

    try:
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Obtém a mensagem
        message = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
            )
            .execute()
        )

        payload = message.get(
            "payload",
            {},
        )

        # Obtém o Subject
        headers = payload.get(
            "headers",
            [],
        )

        subject = "arquivo"

        for header in headers:
            if header.get("name", "").lower() == "subject":
                subject = header.get(
                    "value",
                    "arquivo",
                )
                break

        # Remove caracteres inválidos
        subject = sanitize_filename(subject)

        # Data e hora da mensagem
        internal_date = message.get(
            "internalDate",
        )

        if internal_date:
            message_datetime = datetime.fromtimestamp(
                int(internal_date) / 1000,
                tz=UTC,
            )

            timestamp = message_datetime.strftime("%Y_%m_%d_%H_%M_%S")

        else:
            timestamp = datetime.now(UTC).strftime("%Y_%m_%d_%H_%M_%S")

        # Obtém as partes da mensagem
        parts = payload.get(
            "parts",
            [],
        )

        saved_files: list[str] = []

        for part in parts:
            filename = part.get(
                "filename",
            )

            if not filename:
                continue

            attachment_id = part.get("body", {}).get("attachmentId")

            if not attachment_id:
                continue

            # Preserva a extensão real do anexo
            extension = Path(filename).suffix.lower()

            new_filename = f"{timestamp}_{subject}{extension}"

            file_path = output_dir / new_filename

            # Verifica se o arquivo já existe
            if file_path.exists():
                logger.info(f"Arquivo já existe, download ignorado: {new_filename}")

                saved_files.append(new_filename)

                continue

            # Obtém o conteúdo do anexo
            attachment = (
                service.users()
                .messages()
                .attachments()
                .get(
                    userId="me",
                    messageId=message_id,
                    id=attachment_id,
                )
                .execute()
            )

            data = base64.urlsafe_b64decode(attachment["data"])

            # Salva o arquivo
            file_path.write_bytes(data)

            saved_files.append(new_filename)

        logger.info(f"Anexo salvo com sucesso: {new_filename}")

        logger.info("Término dos downloads dos anexos")

        return saved_files

    except Exception as exc:
        raise RuntimeError(f"Erro ao salvar anexos da mensagem {message_id}.") from exc
