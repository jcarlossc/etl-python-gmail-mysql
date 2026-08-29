from etl_python_gmail_mysql.utils.settings.Settings import Settings


def test_settings_load(monkeypatch):
    """
    Deve carregar corretamente as variáveis de ambiente.
    """

    monkeypatch.setenv("SCOPES", "abc123")
    monkeypatch.setenv("MYSQL_HOST", "localhost")
    monkeypatch.setenv("MYSQL_PORT", "3306")
    monkeypatch.setenv("MYSQL_DATABASE", "empresa")
    monkeypatch.setenv("MYSQL_USER", "root")
    monkeypatch.setenv("MYSQL_PASSWORD", "123456")

    settings = Settings()

    assert settings.scopes == "abc123"
    assert settings.mysql_host == "localhost"
    assert settings.mysql_host == "localhost"
    assert settings.mysql_port == 3306
    assert settings.mysql_database == "empresa"
    assert settings.mysql_user == "root"
    assert settings.mysql_password == "123456"
