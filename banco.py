import sqlite3
try:
    conexao= sqlite3.connect('fioeflor.db')
    cursor = conexao.cursor()
    print("Conectado ao banco")

    #TABELA ESTOQUE
    cursor.execute("""
    CREATE TABLE if not exists estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL,
    sobrenome TEXT NOT NULL,
    endereco TEXT NOT NULL
    )
    """)

    #TABELA FORNECEDOR
    cursor.execute("""
    CREATE TABLE if not exists fornecedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    nome TEXT NOT NULL
    )
    """)
    conexao.commit()
except Exception as erro:
    print('erro', erro)
    exit()