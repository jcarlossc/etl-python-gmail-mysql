import logging

from googleapiclient.discovery import Resource


def get_label_id(
    service: Resource,
    label_name: str,
) -> str:
    """
    Obtém o ID de uma label do Gmail pelo nome.

    Args:
        service: Serviço autenticado da API do Gmail.
        label_name: Nome da label que será localizada.

    Returns:
        str: ID da label encontrada.

    Raises:
        RuntimeError: Se a label não for encontrada ou ocorrer
            um erro ao consultar a API do Gmail.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando aquisição de ID de labels")

    try:
        # Consulta as labels disponíveis na conta autenticada.
        response = service.users().labels().list(userId="me").execute()

        # Procura pela label utilizando o nome informado.
        for label in response["labels"]:
            if label["name"] == label_name:
                logger.info(f"Labels adiquiridas con sucesso: {label_name}")

                return label["id"]

        # Nenhuma label correspondente foi encontrada.
        raise RuntimeError(f"Label '{label_name}' não encontrada.")

    except RuntimeError:
        # Mantém a mensagem específica da label não encontrada.
        raise

    except Exception as exc:
        # Converte erros da API em uma exceção específica da aplicação.
        raise RuntimeError(f"Erro ao buscar label '{label_name}'.") from exc
