import logging
from pathlib import Path
from typing import Any


def setup_logger(logging_config: dict[str, Any]) -> None:
    logger = logging.getLogger(__name__)

    try:
        Path(logging_config["logs"]["file"]).parent.mkdir(parents=True, exist_ok=True)

        level = getattr(logging, logging_config["logging"]["level"], logging.INFO)

        logging.basicConfig(
            level=level,
            format=logging_config["logging"]["format"],
            handlers=[
                logging.FileHandler(
                    logging_config["logs"]["file"],
                    encoding=logging_config["logging"]["encoding"],
                ),
                logging.StreamHandler(),
            ],
        )

        logger.info("Logger configurado com sucesso.")

    except (KeyError, TypeError) as error:
        raise ValueError(f"CONFIG_ERROR: configuração inválida -> {error}") from error

    except OSError as error:
        raise OSError(
            f"FILE_ERROR: erro no arquivo de log '{logging_config}' -> {error}"
        ) from error
