from pathlib import Path
from typing import Any

import yaml


def load_all_configs(config_path: Path) -> dict[str, Any]:
    configs: dict[str, Any] = {}

    try:
        if not config_path.exists():
            raise FileNotFoundError(
                f"Diretório de configuração não encontrado: {config_path}"
            )

        if not config_path.is_dir():
            raise NotADirectoryError(
                f"Caminho informado não é diretório: {config_path}"
            )

        for file in config_path.glob("*.yaml"):
            with open(file, "r", encoding="utf-8") as f:
                configs[file.stem] = yaml.safe_load(f)

        return configs

    except yaml.YAMLError as error:
        raise ValueError(f"YAML_ERROR: erro ao processar YAML -> {error}") from error
