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
    logger = logging.getLogger(__name__)

    logger.info("Iniciando download de anexos")

    try:
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

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

        subject = sanitize_filename(subject)

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

            extension = Path(filename).suffix.lower()

            new_filename = f"{timestamp}_{subject}{extension}"

            file_path = output_dir / new_filename

            if file_path.exists():
                print(f"Arquivo já existe, download ignorado: {new_filename}")

                saved_files.append(new_filename)

                continue

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

            file_path.write_bytes(data)

            saved_files.append(new_filename)

            print(f"Anexo salvo: {file_path}")

        logger.info(f"Anexo baixado com sucesso: {new_filename}")

        logger.info("Término dos downloads dos anexos")

        return saved_files

    except Exception as exc:
        raise RuntimeError(f"Erro ao salvar anexos da mensagem {message_id}.") from exc
