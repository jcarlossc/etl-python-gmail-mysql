import logging
from typing import Any

import pandas as pd


def get_validate_types(
    df: pd.DataFrame, columns_config: dict[str, Any]
) -> pd.DataFrame:
    """
    Converte as colunas dos DataFrames de vendas e clientes.

    A função:
    - Não altera o DataFrame original.
    - Converte IDs para Int64.
    - Converte quantidade para Int64.
    - Converte preços e totais para float64.
    - Converte data_venda para datetime64.
    - Converte colunas textuais para string.
    - Registra problemas de conversão no log.
    - Não realiza limpeza de dados.

    Args:
        df: DataFrame contendo dados de vendas ou clientes.

    Returns:
        DataFrame com os tipos convertidos.

    Raises:
        TypeError: Se o argumento não for um DataFrame.
        ValueError: Se ocorrer um erro durante a conversão.
    """

    logger = logging.getLogger(__name__)

    logger.info("Iniciando conversão de tipos")

    # Validação do tipo de entrada.
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O argumento df deve ser um pandas DataFrame.")

    # Cria uma cópia para preservar o DataFrame original.
    result = df.copy()

    # Tipos esperados para as colunas de vendas.
    sales_types = columns_config["sales_types"]
    customer_types = columns_config["customer_types"]

    # Junta os dois dicionários de tipos.
    # Se uma coluna existir nos dois, o tipo será o mesmo.
    expected_types = {**sales_types, **customer_types}

    try:
        # Converte somente as colunas que existem no DataFrame.
        # Isso permite usar a função tanto para vendas quanto para clientes.
        for column, dtype in expected_types.items():
            if column not in result.columns:
                continue

            if dtype == "datetime64[ns]":
                # Converte datas para datetime.
                # errors="raise" faz a função informar se houver valor inválido.
                result[column] = pd.to_datetime(
                    result[column],
                    errors="raise",
                )

            elif dtype == "Int64":
                # Converte IDs e quantidade para inteiros anuláveis.
                # O pandas Int64 permite valores pd.NA.
                result[column] = result[column].astype("Int64")

            else:
                # Converte strings, preços e totais.
                result[column] = result[column].astype(dtype)

        logger.info("Tipos dos dados convertidos com sucesso.")

        return result

    except (TypeError, ValueError, OverflowError) as error:
        # Registra o problema para facilitar a identificação da coluna.
        logger.exception("Erro durante a conversão dos tipos dos dados.")

        # Mantém a exceção original como causa.
        raise ValueError("Não foi possível converter os tipos dos dados.") from error
