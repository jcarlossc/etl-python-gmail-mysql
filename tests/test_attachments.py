from pathlib import Path
from unittest.mock import MagicMock

from etl_python_gmail_mysql.services.gmail.attachments import save_attachments


def test_save_attachments_salva_anexo(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Testa o download e salvamento de um anexo do Gmail.
    """

    # Cria o conteúdo que será retornado pela API.
    file_content = b"conteudo do arquivo"

    # Mock do serviço do Gmail.
    service = MagicMock()

    # Configura a resposta da mensagem.
    service.users().messages().get().execute.return_value = {
        "payload": {
            "headers": [
                {
                    "name": "Subject",
                    "value": "Relatório de Vendas",
                },
            ],
            "parts": [
                {
                    "filename": "vendas.xlsx",
                    "body": {
                        "attachmentId": "attachment-123",
                    },
                },
            ],
        },
        "internalDate": "1755784800000",
    }

    # Configura a resposta do anexo.
    service.users().messages().attachments().get().execute.return_value = {
        "data": "Y29udGV1ZG8gZG8gYXJxdWl2bw==",
    }

    # Executa a função.
    result = save_attachments(
        service=service,
        message_id="message-123",
        output_dir=tmp_path,
    )

    # Verifica que um arquivo foi salvo.
    assert len(result) == 1

    filename = result[0]

    # Verifica a extensão.
    assert filename.endswith(".xlsx")

    # Verifica que o arquivo realmente existe.
    file_path = tmp_path / filename

    assert file_path.exists()

    # Verifica o conteúdo.
    assert file_path.read_bytes() == file_content
