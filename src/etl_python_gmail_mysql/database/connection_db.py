import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from etl_python_gmail_mysql.utils.settings.Settings import Settings


def get_engine(settings: Settings) -> Engine:
    """
    Cria e retorna uma Engine do SQLAlchemy para conexão com o MySQL.

    Parameters
    ----------
    settings : Settings
        Objeto contendo as configurações de conexão com o banco de dados.

    Returns
    -------
    Engine
        Instância configurada da Engine do SQLAlchemy.

    Raises
    ------
    SQLAlchemyError
        Caso ocorra erro ao criar a Engine.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando criação da engine.")

    try:
        # Monta string de conexão utilizada
        # pelo SQLAlchemy para acessar MySQL.
        conn = (
            f"mysql+pymysql://"
            f"{settings.mysql_user}:"
            f"{settings.mysql_password}@"
            f"{settings.mysql_host}:"
            f"{settings.mysql_port}/"
            # f"{settings.mysql_database}"
        )

        # Cria instância Engine
        engine = create_engine(conn)

        logger.info("Engine criada com sucesso.")

        return engine

    except SQLAlchemyError as error:
        logger.error(f"Erro ao criar engine: {error}")

        raise
