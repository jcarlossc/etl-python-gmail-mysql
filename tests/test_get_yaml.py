from pathlib import Path

import pytest

from etl_python_gmail_mysql.utils.yaml.get_yaml import load_all_configs


def test_load_all_configs_success(tmp_path):
    """
    Verifica se todos os arquivos YAML do diretório
    são carregados corretamente.
    """

    (tmp_path / "logging.yaml").write_text(
        "level: INFO",
        encoding="utf-8",
    )

    # Executa a função.
    configs = load_all_configs(tmp_path)

    # Verifica se os arquivos foram carregados.
    assert "logging" in configs

    # Verifica o conteúdo carregado.
    assert configs["logging"]["level"] == "INFO"


def test_load_all_configs_directory_not_found():
    """
    Verifica se FileNotFoundError é lançado quando
    o diretório informado não existe.
    """

    config_path = Path("diretorio_inexistente")

    with pytest.raises(FileNotFoundError):
        load_all_configs(config_path)


def test_load_all_configs_not_directory(tmp_path):
    """
    Verifica se NotADirectoryError é lançado quando
    o caminho informado não é um diretório.
    """

    # Cria um arquivo comum.
    file = tmp_path / "config.yaml"
    file.write_text("teste", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        load_all_configs(file)


def test_load_all_configs_invalid_yaml(tmp_path):
    """
    Verifica se ValueError é lançado quando
    um arquivo YAML possui sintaxe inválida.
    """

    # Cria um YAML inválido.
    (tmp_path / "config.yaml").write_text(
        "host: localhost\nporta: [1,2",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="YAML_ERROR"):
        load_all_configs(tmp_path)
