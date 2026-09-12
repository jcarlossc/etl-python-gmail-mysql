import pandas as pd


def get_integrate_sales_clients(
    df_sales: pd.DataFrame,
    df_clients: pd.DataFrame,
) -> pd.DataFrame:
    """Integra os dados de vendas com os dados dos clientes.

    Realiza uma junção do tipo left utilizando a coluna
    ``id_cliente``. Cada cliente deve possuir um único registro,
    enquanto uma venda pode estar associada a um ou mais registros
    de vendas.

    Args:
        df_sales: DataFrame contendo os dados das vendas.
        df_clients: DataFrame contendo os dados dos clientes.

    Returns:
        DataFrame contendo os dados de vendas integrados aos
        dados dos clientes.

    Raises:
        RuntimeError: Se ocorrer um erro durante a integração.
    """

    try:
        # Integra as vendas aos clientes pelo identificador do cliente.
        # many_to_one garante que cada cliente apareça uma única vez.
        df_integrated = df_sales.merge(
            df_clients,
            on="id_cliente",
            how="left",
            validate="many_to_one",
        )

        return df_integrated

    except Exception as exc:
        raise RuntimeError(f"Erro ao integrar vendas e clientes: {exc}") from exc
