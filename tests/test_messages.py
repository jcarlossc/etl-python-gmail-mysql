from unittest.mock import MagicMock

import pytest

from etl_python_gmail_mysql.services.gmail.messages import get_messages


def test_get_messages_returns_messages() -> None:
    """Deve retornar as mensagens encontradas."""
    service = MagicMock()

    service.users().messages().list().execute.return_value = {
        "messages": [
            {"id": "123"},
            {"id": "456"},
        ]
    }

    result = get_messages(
        service=service,
        label_id="INBOX",
    )

    assert result == [
        {"id": "123"},
        {"id": "456"},
    ]


def test_get_messages_returns_empty_list_when_no_messages() -> None:
    """Deve retornar lista vazia quando não houver mensagens."""
    service = MagicMock()

    service.users().messages().list().execute.return_value = {}

    result = get_messages(
        service=service,
        label_id="INBOX",
    )

    assert result == []


def test_get_messages_raises_runtime_error() -> None:
    """Deve lançar RuntimeError quando ocorrer erro na API."""
    service = MagicMock()

    service.users().messages().list().execute.side_effect = Exception("Erro na API")

    with pytest.raises(
        RuntimeError,
        match="Erro ao listar mensagens",
    ):
        get_messages(
            service=service,
            label_id="INBOX",
        )
