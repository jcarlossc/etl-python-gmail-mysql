import logging
from typing import Any

from googleapiclient.discovery import Resource


def get_messages(
    service: Resource,
    label_id: str,
) -> list[dict[str, Any]]:
    """
    Obtém as mensagens associadas a uma label do Gmail.

    Args:
        service: Serviço autenticado da Gmail API.
        label_id: ID da label utilizada para filtrar as mensagens.

    Returns:
        Lista de mensagens retornadas pela Gmail API.
        Retorna uma lista vazia caso nenhuma mensagem seja encontrada.

    Raises:
        RuntimeError: Se ocorrer erro durante a consulta à Gmail API.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando aquisição de mensagens de labels")

    try:
        # Consulta as mensagens associadas à label informada.
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                labelIds=[label_id],
            )
            .execute()
        )

        logger.info("Mensagens adiquiridas com sucesso")

        # Retorna as mensagens encontradas.
        # Caso a API não retorne a chave "messages",
        # retorna uma lista vazia.
        return response.get(
            "messages",
            [],
        )

    except Exception as exc:
        # Converte qualquer erro da API em uma exceção
        # específica do domínio da aplicação.
        raise RuntimeError("Erro ao listar mensagens.") from exc
