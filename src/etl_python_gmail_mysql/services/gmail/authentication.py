import logging
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build


def get_gmail_service(
    scopes: list[str],
    base_dir: Path,
    credentials_file: Path,
    token_file: Path,
) -> Resource:
    """
    Autentica no Gmail e retorna o serviço da API.

    Utiliza um token existente quando disponível. Caso o token
    esteja expirado e possua refresh token, tenta renová-lo.
    Se não houver credenciais válidas, inicia o fluxo OAuth local.

    Args:
        scopes: Lista de permissões solicitadas à API do Gmail.
        base_dir: Diretório base utilizado pela aplicação.
        credentials_file: Arquivo JSON das credenciais OAuth.
        token_file: Arquivo onde o token autenticado será armazenado.

    Returns:
        Serviço autenticado da API do Gmail.

    Raises:
        FileNotFoundError: Se o arquivo de credenciais não existir.
        ValueError: Se as credenciais não puderem ser carregadas.
        OSError: Se houver erro ao ler ou gravar arquivos.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando autenticação no Gmail")

    # Garante que o diretório base exista.
    base_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    credentials = None

    try:
        # Tenta carregar um token já existente.
        if token_file.exists():
            credentials = Credentials.from_authorized_user_file(
                token_file,
                scopes,
            )

        # Verifica se as credenciais atuais são válidas.
        if not credentials or not credentials.valid:
            # Renova o token quando possível.
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())

            else:
                # Inicia o fluxo OAuth para obter novas credenciais.
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file,
                    scopes,
                )

                credentials = flow.run_local_server(
                    port=0,
                )

            # Salva o token para reutilização futura.
            token_file.write_text(
                credentials.to_json(),
                encoding="utf-8",
            )

        logger.info("Gmail autenticado com sucesso")

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
