from googleapiclient.discovery import Resource


def get_label_id(
    service: Resource,
    label_name: str,
) -> str:
    try:
        response = service.users().labels().list(userId="me").execute()

        for label in response["labels"]:
            if label["name"] == label_name:
                return label["id"]

        raise RuntimeError(f"Label '{label_name}' não encontrada.")

    except RuntimeError:
        raise

    except Exception as exc:
        raise RuntimeError(f"Erro ao buscar label '{label_name}'.") from exc
