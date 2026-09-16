import logging

from etl_python_gmail_mysql.pipeline.run_pipeline import get_run_pipeline


def main() -> None:
    """
    Ponto de entrada principal da aplicação.

    Executa o pipeline ETL.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando aplicação.")

    get_run_pipeline()

    logger.info("Aplicação finalizada com sucesso.")


if __name__ == "__main__":
    main()
