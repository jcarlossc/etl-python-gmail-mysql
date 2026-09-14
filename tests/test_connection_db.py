from sqlalchemy.exc import SQLAlchemyError

from etl_python_gmail_mysql.database.connection_db import get_engine
from etl_python_gmail_mysql.utils.settings.Settings import Settings


def test_get_engine_success(monkeypatch):
    # Configuração simulada da conexão
    settings = Settings(
        mysql_user="root",
        mysql_password="1234",
        mysql_host="localhost",
        mysql_port=3306,
        mysql_database="teste",
    )

    # Simula a criação da Engine
    class FakeEngine:
        pass

    monkeypatch.setattr(
        "etl_python_gmail_mysql.database.connection_db.create_engine",
        lambda conn: FakeEngine(),
    )

    # Executa a função
    engine = get_engine(settings)

    # Verifica se a Engine foi criada
    assert isinstance(engine, FakeEngine)


def test_get_engine_error(monkeypatch):
    # Configuração simulada da conexão
    settings = Settings(
        mysql_user="root",
        mysql_password="1234",
        mysql_host="localhost",
        mysql_port=3306,
        mysql_database="teste",
    )

    # Simula erro ao criar a Engine
    def fake_create_engine(conn):
        raise SQLAlchemyError("Erro de conexão")

    monkeypatch.setattr(
        "etl_python_gmail_mysql.database.connection_db.create_engine",
        fake_create_engine,
    )

    # Verifica se a exceção é propagada
    import pytest

    with pytest.raises(SQLAlchemyError):
        get_engine(settings)
