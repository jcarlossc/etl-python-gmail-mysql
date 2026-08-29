from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Representa as configurações da aplicação.

    Todos os atributos são carregados automaticamente do
    arquivo .env.
    """

    # Autenticação Gmail
    scopes: str

    # Endereço do servidor MySQL.
    mysql_host: str

    # Porta utilizada pelo servidor MySQL.
    mysql_port: int = 3306

    # Usuário do banco.
    mysql_user: str

    # Senha do banco.
    mysql_password: str

    # Nome do banco de dados
    mysql_database: str

    # Configuração do Pydantic.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


def get_settings() -> Settings:
    """
    Cria uma instância das configurações da aplicação.

    Returns
    -------
    Settings
        Objeto contendo as configurações carregadas do arquivo .env.
    """
    return Settings()
