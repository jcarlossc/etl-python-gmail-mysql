from pathlib import Path

from etl_python_gmail_mysql.services.gmail.authentication import get_gmail_service


def test_get_gmail_service_com_token_valido(
    tmp_path: Path,
    monkeypatch,
):
    """Deve criar o serviço utilizando um token válido existente."""

    token_file = tmp_path / "token.json"
    credentials_file = tmp_path / "credentials.json"

    token_file.write_text(
        '{"token": "fake-token"}',
        encoding="utf-8",
    )

    credentials_file.write_text(
        "{}",
        encoding="utf-8",
    )

    class FakeCredentials:
        valid = True
        expired = False
        refresh_token = None

        def to_json(self):
            return '{"token": "fake-token"}'

    fake_credentials = FakeCredentials()

    def fake_from_authorized_user_file(
        filename,
        scopes,
    ):
        return fake_credentials

    def fake_build(
        service_name,
        version,
        credentials,
    ):
        return {
            "service": service_name,
            "version": version,
            "credentials": credentials,
        }

    monkeypatch.setattr(
        "etl_python_gmail_mysql.services.gmail.authentication.Credentials.from_authorized_user_file",
        fake_from_authorized_user_file,
    )

    monkeypatch.setattr(
        "etl_python_gmail_mysql.services.gmail.authentication.build",
        fake_build,
    )

    service = get_gmail_service(
        scopes=["gmail.readonly"],
        base_dir=tmp_path,
        credentials_file=credentials_file,
        token_file=token_file,
    )

    assert service["service"] == "gmail"
    assert service["version"] == "v1"
    assert service["credentials"] is fake_credentials
