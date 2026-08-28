from pathlib import Path
from typing import Any

import yaml


def load_all_configs(config_path: Path) -> dict[str, Any]:
    """
    Carrega todos os arquivos de configuração YAML presentes
    em um diretório específico.

    Esta função percorre o diretório informado, identifica
    todos os arquivos com extensão `.yaml` e os carrega para
    um dicionário Python. Cada arquivo é armazenado utilizando
    o nome do arquivo (sem extensão) como chave.

    Parâmetros
    ----------
    config_path : Path
        Caminho para o diretório que contém os arquivos de configuração.

    Retorno
    -------
    Dict[str, Any]
        Dicionário contendo todas as configurações carregadas.
        A chave corresponde ao nome do arquivo YAML e o valor
        corresponde ao conteúdo do arquivo convertido para
        estrutura Python.

    Observações
    -----------
    Essa função é utilizada para centralizar o carregamento de
    configurações do projeto, permitindo separar parâmetros
    do código-fonte. Essa abordagem é comum em pipelines de
    dados e aplicações que utilizam arquivos YAML para definir
    caminhos, parâmetros de execução e configurações de logging.
    """

    # Inicializa o dicionário que armazenará todas as configurações
    # carregadas a partir dos arquivos YAML.
    configs: dict[str, Any] = {}

    try:
        # Verifica se o diretório de configuração existe.
        if not config_path.exists():
            raise FileNotFoundError(
                f"Diretório de configuração não encontrado: {config_path}"
            )

        if not config_path.is_dir():
            raise NotADirectoryError(
                f"Caminho informado não é diretório: {config_path}"
            )

        # Percorre todos os arquivos com extensão .yaml
        for file in config_path.glob("*.yaml"):
            # Abre o arquivo YAML em modo leitura utilizando
            # codificação UTF-8 para garantir compatibilidade.
            with open(file, "r", encoding="utf-8") as f:
                # Carrega o conteúdo YAML de forma segura utilizando
                # yaml.safe_load, que evita execução de código arbitrário.
                configs[file.stem] = yaml.safe_load(f)

        return configs

    except yaml.YAMLError as error:
        raise ValueError(f"YAML_ERROR: erro ao processar YAML -> {error}") from error
