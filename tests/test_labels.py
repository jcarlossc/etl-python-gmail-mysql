from unittest.mock import MagicMock

import pytest

from etl_python_gmail_mysql.services.gmail.labels import get_label_id


def test_get_label_id_label_encontrada() -> None:
    """Deve retornar o ID quando a label for encontrada."""

    # Simula a resposta da API do Gmail.
    service = MagicMock()

    service.users().labels().list().execute.return_value = {
        "labels": [
            {
                "id": "Label_123",
                "name": "EMPRESA",
            },
            {
                "id": "Label_456",
                "name": "INBOX",
            },
        ]
    }

    # Executa a função.
    result = get_label_id(
        service=service,
        label_name="EMPRESA",
    )

    # Verifica se o ID correto foi retornado.
    assert result == "Label_123"


def test_get_label_id_label_nao_encontrada() -> None:
    """Deve lançar RuntimeError quando a label não existir."""

    # Simula uma resposta sem a label procurada.
    service = MagicMock()

    service.users().labels().list().execute.return_value = {
        "labels": [
            {
                "id": "Label_123",
                "name": "INBOX",
            }
        ]
    }

    # Verifica se a exceção esperada é lançada.
    with pytest.raises(
        RuntimeError,
        match="Label 'EMPRESA' não encontrada.",
    ):
        get_label_id(
            service=service,
            label_name="EMPRESA",
        )


def test_get_label_id_erro_na_api() -> None:
    """Deve lançar RuntimeError quando a API apresentar erro."""

    # Simula uma falha durante a chamada da API.
    service = MagicMock()

    service.users().labels().list().execute.side_effect = Exception("Erro de conexão")

    # Verifica se o erro é convertido para RuntimeError.
    with pytest.raises(
        RuntimeError,
        match="Erro ao buscar label 'EMPRESA'.",
    ):
        get_label_id(
            service=service,
            label_name="EMPRESA",
        )
