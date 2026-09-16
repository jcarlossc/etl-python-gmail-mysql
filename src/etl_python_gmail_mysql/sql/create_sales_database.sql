DROP DATABASE IF EXISTS gmail_database;

CREATE DATABASE gmail_database
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE gmail_database;

-- ==========================
-- DIM_CLIENTE
-- ==========================
CREATE TABLE dim_cliente (

    sk_cliente INT PRIMARY KEY,

    id_cliente INT NOT NULL,

    nome VARCHAR(255) NOT NULL,

    email VARCHAR(255),

    cidade VARCHAR(100),

    estado CHAR(2),

    UNIQUE(id_cliente)

);

-- ==========================
-- DIM_PRODUTO
-- ==========================
CREATE TABLE dim_produto (

    sk_produto INT PRIMARY KEY,

    produto VARCHAR(255) NOT NULL,

    UNIQUE(produto)

);

-- ==========================
-- DIM_TEMPO
-- ==========================
CREATE TABLE dim_tempo (

    sk_tempo INT PRIMARY KEY,

    data_venda DATE NOT NULL,

    ano INT NOT NULL,

    mes INT NOT NULL,

    dia INT NOT NULL,

    UNIQUE(data_venda)

);

-- ==========================
-- FATO_VENDAS
-- ==========================
CREATE TABLE fato_vendas (

    id_venda BIGINT PRIMARY KEY,

    sk_cliente INT NOT NULL,

    sk_produto INT NOT NULL,

    sk_tempo INT NOT NULL,

    quantidade INT NOT NULL,

    preco_unitario DECIMAL(18,2) NOT NULL,

    total DECIMAL(18,2) NOT NULL,

    CONSTRAINT fk_vendas_cliente
        FOREIGN KEY (sk_cliente)
        REFERENCES dim_cliente(sk_cliente),

    CONSTRAINT fk_vendas_produto
        FOREIGN KEY (sk_produto)
        REFERENCES dim_produto(sk_produto),

    CONSTRAINT fk_vendas_tempo
        FOREIGN KEY (sk_tempo)
        REFERENCES dim_tempo(sk_tempo)

);

-- ==========================
-- ÍNDICES
-- ==========================

CREATE INDEX idx_fato_vendas_cliente
ON fato_vendas(sk_cliente);

CREATE INDEX idx_fato_vendas_produto
ON fato_vendas(sk_produto);

CREATE INDEX idx_fato_vendas_tempo
ON fato_vendas(sk_tempo);
