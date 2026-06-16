import psycopg2
import os
try:
    conexao= psycopg2.connect(
        'postgresql://fioflor_user:HovUbDHO8DqWThqfnsQOiWRVqH4qqt6T@dpg-d8osui9194ac738nsa90-a.virginia-postgres.render.com/fioflor')
    cursor = conexao.cursor()

    print("Conectado ao banco")

    #TABELA ESTOQUE
    cursor.execute("""
    CREATE TABLE if not exists estoque (
    id SERIAL PRIMARY KEY NOT NULL,
    modelo TEXT NOT NULL,
    tamanho text NOT NULL,
    fornecedor_id INTEGER NOT NULL,
    quantidade INTEGER,
    preco real,
    preco_custo real
    )
    """)

    #TABELA CLIENTES
    cursor.execute("""
    CREATE TABLE if not exists clientes (
    id SERIAL PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    endereco TEXT NOT NULL
    )
    """)

    #TABELA FORNECEDOR
    cursor.execute("""
    CREATE TABLE if not exists fornecedor (
    id SERIAL PRIMARY KEY NOT NULL,
    nome TEXT NOT NULL
    )
    """)

    #TABELA CAIXA
    cursor.execute("""
    CREATE TABLE if not exists caixa (
        id SERIAL PRIMARY KEY NOT NULL,
        produto_id INTEGER,
        tipo TEXT NOT NULL,
        quantidade INTEGER,
        valor_total REAL,
        data_movimentacao TEXT,
        foreign key (produto_id) references estoque(id)
        )
        """)
    conexao.commit()
except Exception as erro:
    print('erro', erro)
    exit()