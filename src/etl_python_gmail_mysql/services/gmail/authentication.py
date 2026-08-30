from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource


def get_gmail_service(
    scopes: list[str],
    base_dir: Path,
    credentials_file: Path,
    token_file: Path,
) -> Resource:
    base_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    credentials = None

    try:
        if token_file.exists():
            credentials = Credentials.from_authorized_user_file(
                token_file,
                scopes,
            )

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file,
                    scopes,
                )

                credentials = flow.run_local_server(
                    port=0,
                )

            token_file.write_text(
                credentials.to_json(),
                encoding="utf-8",
            )

        return build(
            "gmail",
            "v1",
            credentials=credentials,
        )

    except FileNotFoundError:
        raise

    except OSError:
        raise

    except Exception as exc:
        raise RuntimeError("Não foi possível autenticar no Gmail.") from exc
