import logging
from pathlib import Path
from typing import Any

import pytest

from etl_python_gmail_mysql.utils.loggers.logger import setup_logger


@pytest.fixture
def logging_config(tmp_path: Path) -> dict[str, Any]:
    """Cria uma configuração de logging para os testes."""
    return {
        "logging": {
            "level": "INFO",
            "format": "%(levelname)s - %(message)s",
            "encoding": "utf-8",
        },
        "logs": {
            "file": str(tmp_path / "app.log"),
        },
    }


def test_setup_logger(
    logging_config: dict[str, Any],
) -> None:
    """Deve configurar o logger e criar o arquivo de log."""
    setup_logger(logging_config)

    log_file = Path(logging_config["logs"]["file"])
    logger = logging.getLogger()

    assert log_file.exists()
    assert logger.level == logging.INFO
    assert logger.handlers


def test_setup_logger_invalid_config() -> None:
    """Deve lançar ValueError para configuração inválida."""
    config = {
        "logging": {
            "level": "INFO",
        },
    }

    with pytest.raises(ValueError, match="CONFIG_ERROR"):
        setup_logger(config)


def test_setup_logger_invalid_log_path(
    logging_config: dict[str, Any],
) -> None:
    """Deve lançar ValueError para caminho de log inválido."""
    logging_config["logs"]["file"] = "\0app.log"

    with pytest.raises(ValueError):
        setup_logger(logging_config)
