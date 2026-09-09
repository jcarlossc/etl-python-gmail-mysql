import pandas as pd


def get_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa inconsistências de um DataFrame de vendas ou clientes.

    A função identifica as colunas existentes e aplica somente
    as regras de limpeza correspondentes.

    Args:
        df: DataFrame previamente validado quanto aos tipos.

    Returns:
        DataFrame limpo e com índice reorganizado.

    Raises:
        TypeError: Se df não for um DataFrame.
        ValueError: Se df estiver vazio.
        RuntimeError: Se ocorrer erro inesperado durante a limpeza.
    """

    try:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df deve ser um pandas.DataFrame.")

        if df.empty:
            raise ValueError("O DataFrame não pode estar vazio.")

        cleaned_df = df.copy()

        # Limpeza de campos textuais
        text_columns = cleaned_df.select_dtypes(include=["object", "string"]).columns

        for column in text_columns:
            cleaned_df[column] = cleaned_df[column].str.strip().replace("", pd.NA)

        # Valores infinitos
        cleaned_df = cleaned_df.replace(
            [float("inf"), float("-inf")],
            pd.NA,
        )

        # Linhas completamente vazias
        cleaned_df = cleaned_df.dropna(how="all")

        # Registros duplicados
        cleaned_df = cleaned_df.drop_duplicates()

        # Regras específicas de vendas
        if "quantidade" in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df["quantidade"] > 0]

        if "preco_unitario" in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df["preco_unitario"] >= 0]

        if "total" in cleaned_df.columns:
            cleaned_df = cleaned_df[cleaned_df["total"] >= 0]

        # Data de venda
        if "data_venda" in cleaned_df.columns:
            cleaned_df["data_venda"] = pd.to_datetime(
                cleaned_df["data_venda"],
                errors="coerce",
            )

        # Índice
        cleaned_df = cleaned_df.reset_index(drop=True)

        return cleaned_df

    except (TypeError, ValueError):
        raise

    except Exception as exc:
        raise RuntimeError("Erro inesperado durante a limpeza do DataFrame.") from exc
