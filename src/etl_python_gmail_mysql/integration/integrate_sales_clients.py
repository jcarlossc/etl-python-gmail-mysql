import pandas as pd


def get_integrate_sales_clients(
    df_sales: pd.DataFrame,
    df_clients: pd.DataFrame,
) -> pd.DataFrame:
    try:
        df_integrated = df_sales.merge(
            df_clients,
            on="id_cliente",
            how="left",
            validate="many_to_one",
        )

        return df_integrated

    except Exception as exc:
        raise RuntimeError(f"Erro ao integrar vendas e clientes: {exc}") from exc
