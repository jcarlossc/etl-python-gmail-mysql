import logging

# from pathlib import Path
from typing import Any

import pandas as pd


def get_validate_types(
    df: pd.DataFrame, columns_config: dict[str, Any]
) -> pd.DataFrame:
    logger = logging.getLogger(__name__)

    logger.info("Iniciando conversão de tipos")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("O argumento df deve ser um pandas DataFrame.")

    result = df.copy()

    sales_types = columns_config["sales_types"]
    customer_types = columns_config["customer_types"]

    expected_types = {**sales_types, **customer_types}

    try:
        for column, dtype in expected_types.items():
            if column not in result.columns:
                continue

            if dtype == "datetime64[ns]":
                result[column] = pd.to_datetime(
                    result[column],
                    errors="raise",
                )

            elif dtype == "Int64":
                result[column] = result[column].astype("Int64")

            else:
                result[column] = result[column].astype(dtype)

        logger.info("Tipos dos dados convertidos com sucesso.")

        return result

    except (TypeError, ValueError, OverflowError) as error:
        logger.exception("Erro durante a conversão dos tipos dos dados.")

        raise ValueError("Não foi possível converter os tipos dos dados.") from error
