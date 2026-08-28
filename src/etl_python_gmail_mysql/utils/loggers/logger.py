import logging
from pathlib import Path
from typing import Any


def setup_logger(logging_config: dict[str, Any]) -> None:
    """
    Configura o sistema de logging da aplicação.

    Esta função inicializa o logger principal utilizando parâmetros
    definidos em arquivos de configuração. O sistema de logging é
    configurado para registrar mensagens tanto no console quanto
    em um arquivo de log persistente.

    Parâmetros
    ----------
    logging_config : Dict[str, Any]
        Dicionário contendo as configurações de logging da aplicação,
        normalmente carregadas a partir de arquivos YAML ou JSON.

    log_file : str
        Caminho do arquivo onde os logs serão persistidos.

    Retorno
    -------
    None
        A função apenas configura o sistema de logging global da
        aplicação e não retorna valores.

    Observações
    -----------
    O logging é configurado utilizando dois handlers:

    - FileHandler: grava logs em arquivo para auditoria e análise posterior.
    - StreamHandler: exibe logs no console para acompanhamento em tempo real.

    Essa abordagem é comum em pipelines de dados e aplicações que
    precisam de monitoramento contínuo e rastreabilidade de execução.
    """

    logger = logging.getLogger(__name__)

    try:
        # Garante que a pasta existe
        Path(logging_config["logs"]["file"]).parent.mkdir(parents=True, exist_ok=True)

        # Obtém o nível de logging definido na configuração.
        # Caso o nível não exista, utiliza INFO como padrão.
        level = getattr(logging, logging_config["logging"]["level"], logging.INFO)

        # Configura o sistema de logging da aplicação.
        # logging.basicConfig inicializa o logger raiz (root logger)
        # com os parâmetros definidos.
        logging.basicConfig(
            # Define o nível mínimo de mensagens que serão registradas.
            level=level,
            # Define o formato das mensagens de log.
            # Normalmente inclui timestamp, nível do log, módulo e mensagem.
            format=logging_config["logging"]["format"],
            # Define os handlers responsáveis por enviar os logs
            # para diferentes destinos.
            handlers=[
                # FileHandler grava os logs em arquivo para posterior auditoria
                # e análise de execução do pipeline.
                logging.FileHandler(
                    logging_config["logs"]["file"],
                    encoding=logging_config["logging"]["encoding"],
                ),
                # StreamHandler envia os logs para o console (stdout),
                # permitindo acompanhar a execução em tempo real.
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
