import pandas as pd


def get_create_star_schema(
    df_integrated: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    try:
        dim_cliente = (
            df_integrated[
                [
                    "id_cliente",
                    "nome",
                    "email",
                    "cidade",
                    "estado",
                ]
            ]
            .drop_duplicates(subset=["id_cliente"])
            .reset_index(drop=True)
        )

        dim_cliente.insert(
            0,
            "sk_cliente",
            range(1, len(dim_cliente) + 1),
        )

        dim_produto = (
            df_integrated[
                [
                    "produto",
                ]
            ]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        dim_produto.insert(
            0,
            "sk_produto",
            range(1, len(dim_produto) + 1),
        )

        dim_tempo = (
            df_integrated[
                [
                    "data_venda",
                ]
            ]
            .drop_duplicates()
            .sort_values("data_venda")
            .reset_index(drop=True)
        )

        dim_tempo["ano"] = dim_tempo["data_venda"].dt.year
        dim_tempo["mes"] = dim_tempo["data_venda"].dt.month
        dim_tempo["dia"] = dim_tempo["data_venda"].dt.day

        dim_tempo.insert(
            0,
            "sk_tempo",
            range(1, len(dim_tempo) + 1),
        )

        fato_vendas = df_integrated[
            [
                "id_venda",
                "id_cliente",
                "produto",
                "data_venda",
                "quantidade",
                "preco_unitario",
                "total",
            ]
        ].copy()

        fato_vendas = fato_vendas.merge(
            dim_cliente[
                [
                    "sk_cliente",
                    "id_cliente",
                ]
            ],
            on="id_cliente",
            how="left",
            validate="many_to_one",
        )

        fato_vendas = fato_vendas.merge(
            dim_produto[
                [
                    "sk_produto",
                    "produto",
                ]
            ],
            on="produto",
            how="left",
            validate="many_to_one",
        )

        fato_vendas = fato_vendas.merge(
            dim_tempo[
                [
                    "sk_tempo",
                    "data_venda",
                ]
            ],
            on="data_venda",
            how="left",
            validate="many_to_one",
        )

        fato_vendas = fato_vendas[
            [
                "id_venda",
                "sk_cliente",
                "sk_produto",
                "sk_tempo",
                "quantidade",
                "preco_unitario",
                "total",
            ]
        ]

        return {
            "dim_cliente": dim_cliente,
            "dim_produto": dim_produto,
            "dim_tempo": dim_tempo,
            "fato_vendas": fato_vendas,
        }

    except Exception as exc:
        raise RuntimeError(f"Erro ao criar Star Schema: {exc}") from exc
