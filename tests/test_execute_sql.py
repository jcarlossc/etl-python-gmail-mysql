from pathlib import Path

import pytest
from sqlalchemy.exc import SQLAlchemyError

from etl_python_gmail_mysql.sql.execute_sql import (
    get_execute_sql,
)


def test_execute_sql_success(
    tmp_path: Path,
) -> None:
    """Testa a execução de um arquivo SQL com sucesso."""

    sql_file = tmp_path / "test.sql"

    sql_file.write_text(
        """
        CREATE TABLE clientes (
            id INT PRIMARY KEY
        );

        CREATE TABLE vendas (
            id INT PRIMARY KEY
        );
        """,
        encoding="utf-8",
    )

    executed_statements = []

    class MockConnection:
        """Simula uma conexão SQLAlchemy."""

        def execute(self, statement):
            """Armazena o comando SQL executado."""
            executed_statements.append(statement)

    class MockTransaction:
        """Simula uma transação SQLAlchemy."""

        def __enter__(self):
            return MockConnection()

        def __exit__(
            self,
            exc_type,
            exc_value,
            traceback,
        ):
            return None

    class MockEngine:
        """Simula uma Engine SQLAlchemy."""

        def begin(self):
            """Inicia uma transação simulada."""
            return MockTransaction()

    engine = MockEngine()

    get_execute_sql(
        engine=engine,
        sql_file=sql_file,
    )

    assert len(executed_statements) == 2


def test_execute_sql_file_not_found(
    tmp_path: Path,
) -> None:
    """Testa erro quando o arquivo SQL não existe."""

    sql_file = tmp_path / "arquivo_inexistente.sql"

    engine = object()

    with pytest.raises(FileNotFoundError):
        get_execute_sql(
            engine=engine,
            sql_file=sql_file,
        )


def test_execute_sql_empty_file(
    tmp_path: Path,
) -> None:
    """Testa erro quando o arquivo SQL está vazio."""

    sql_file = tmp_path / "empty.sql"

    sql_file.write_text(
        "",
        encoding="utf-8",
    )

    engine = object()

    with pytest.raises(
        ValueError,
        match="Arquivo SQL vazio ou sem comandos",
    ):
        get_execute_sql(
            engine=engine,
            sql_file=sql_file,
        )


def test_execute_sql_sqlalchemy_error(
    tmp_path: Path,
) -> None:
    """Testa erro do SQLAlchemy durante a execução do SQL."""

    sql_file = tmp_path / "test.sql"

    sql_file.write_text(
        "CREATE TABLE clientes (id INT);",
        encoding="utf-8",
    )

    class MockConnection:
        """Simula uma conexão SQLAlchemy com erro."""

        def execute(self, statement):
            """Simula erro durante a execução SQL."""
            raise SQLAlchemyError("Erro ao executar SQL")

    class MockTransaction:
        """Simula uma transação SQLAlchemy."""

        def __enter__(self):
            return MockConnection()

        def __exit__(
            self,
            exc_type,
            exc_value,
            traceback,
        ):
            return None

    class MockEngine:
        """Simula uma Engine SQLAlchemy."""

        def begin(self):
            """Inicia uma transação simulada."""
            return MockTransaction()

    engine = MockEngine()

    with pytest.raises(
        RuntimeError,
        match="Erro ao executar script SQL",
    ):
        get_execute_sql(
            engine=engine,
            sql_file=sql_file,
        )
