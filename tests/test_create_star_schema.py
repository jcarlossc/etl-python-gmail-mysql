import pandas as pd

from etl_python_gmail_mysql.schema.create_star_schema import (
    get_create_star_schema,
)


def get_df_integrated() -> pd.DataFrame:
    """Cria um DataFrame integrado para os testes."""

    return pd.DataFrame(
        {
            "id_venda": [1, 2, 3, 4],
            "id_cliente": [10, 20, 10, 30],
            "produto": [
                "Mouse",
                "Teclado",
                "Mouse",
                "Monitor",
            ],
            "data_venda": pd.to_datetime(
                [
                    "2026-01-01",
                    "2026-01-02",
                    "2026-01-01",
                    "2026-02-15",
                ]
            ),
            "quantidade": [1, 2, 3, 1],
            "preco_unitario": [
                80.0,
                150.0,
                80.0,
                900.0,
            ],
            "total": [
                80.0,
                300.0,
                240.0,
                900.0,
            ],
            "nome": [
                "Carlos",
                "João",
                "Carlos",
                "Maria",
            ],
            "email": [
                "carlos@example.com",
                "joao@example.com",
                "carlos@example.com",
                "maria@example.com",
            ],
            "cidade": [
                "Recife",
                "Olinda",
                "Recife",
                "Jaboatão",
            ],
            "estado": [
                "PE",
                "PE",
                "PE",
                "PE",
            ],
        }
    )


def test_get_create_star_schema_returns_tables() -> None:
    """Testa se o Star Schema retorna as quatro tabelas."""

    df_integrated = get_df_integrated()

    result = get_create_star_schema(
        df_integrated=df_integrated,
    )

    assert isinstance(result, dict)

    assert "dim_cliente" in result
    assert "dim_produto" in result
    assert "dim_tempo" in result
    assert "fato_vendas" in result


def test_dim_cliente() -> None:
    """Testa a estrutura da dimensão de clientes."""

    df_integrated = get_df_integrated()

    result = get_create_star_schema(
        df_integrated=df_integrated,
    )

    dim_cliente = result["dim_cliente"]

    assert list(dim_cliente.columns) == [
        "sk_cliente",
        "id_cliente",
        "nome",
        "email",
        "cidade",
        "estado",
    ]

    assert len(dim_cliente) == 3

    assert dim_cliente["id_cliente"].is_unique
    assert dim_cliente["sk_cliente"].is_unique

    assert dim_cliente["sk_cliente"].tolist() == [1, 2, 3]


def test_dim_produto() -> None:
    """Testa a estrutura da dimensão de produtos."""

    df_integrated = get_df_integrated()

    result = get_create_star_schema(
        df_integrated=df_integrated,
    )

    dim_produto = result["dim_produto"]

    assert list(dim_produto.columns) == [
        "sk_produto",
        "produto",
    ]

    assert len(dim_produto) == 3

    assert dim_produto["produto"].is_unique
    assert dim_produto["sk_produto"].is_unique

    assert dim_produto["sk_produto"].tolist() == [1, 2, 3]


def test_dim_tempo() -> None:
    """Testa a estrutura da dimensão de tempo."""

    df_integrated = get_df_integrated()

    result = get_create_star_schema(
        df_integrated=df_integrated,
    )

    dim_tempo = result["dim_tempo"]

    assert list(dim_tempo.columns) == [
        "sk_tempo",
        "data_venda",
        "ano",
        "mes",
        "dia",
    ]

    assert len(dim_tempo) == 3

    assert dim_tempo["data_venda"].is_unique
    assert dim_tempo["sk_tempo"].is_unique

    assert dim_tempo["sk_tempo"].tolist() == [1, 2, 3]

    assert dim_tempo["ano"].tolist() == [
        2026,
        2026,
        2026,
    ]

    assert dim_tempo["mes"].tolist() == [
        1,
        1,
        2,
    ]

    assert dim_tempo["dia"].tolist() == [
        1,
        2,
        15,
    ]


def test_fato_vendas() -> None:
    """Testa a estrutura da tabela fato de vendas."""

    df_integrated = get_df_integrated()

    result = get_create_star_schema(
        df_integrated=df_integrated,
    )

    fato_vendas = result["fato_vendas"]

    assert list(fato_vendas.columns) == [
        "id_venda",
        "sk_cliente",
        "sk_produto",
        "sk_tempo",
        "quantidade",
        "preco_unitario",
        "total",
    ]

    assert len(fato_vendas) == 4

    assert fato_vendas["id_venda"].is_unique

    assert fato_vendas["sk_cliente"].notna().all()
    assert fato_vendas["sk_produto"].notna().all()
    assert fato_vendas["sk_tempo"].notna().all()


def test_fato_vendas_foreign_keys() -> None:
    """Testa a integridade das chaves da tabela fato."""

    df_integrated = get_df_integrated()

    result = get_create_star_schema(
        df_integrated=df_integrated,
    )

    dim_cliente = result["dim_cliente"]
    dim_produto = result["dim_produto"]
    dim_tempo = result["dim_tempo"]
    fato_vendas = result["fato_vendas"]

    assert fato_vendas["sk_cliente"].isin(dim_cliente["sk_cliente"]).all()

    assert fato_vendas["sk_produto"].isin(dim_produto["sk_produto"]).all()

    assert fato_vendas["sk_tempo"].isin(dim_tempo["sk_tempo"]).all()
