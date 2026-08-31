from typing import Any

from googleapiclient.discovery import Resource


def get_messages(
    service: Resource,
    label_id: str,
) -> list[dict[str, Any]]:
    try:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                labelIds=[label_id],
            )
            .execute()
        )

        return response.get(
            "messages",
            [],
        )

    except Exception as exc:
        raise RuntimeError("Erro ao listar mensagens.") from exc
