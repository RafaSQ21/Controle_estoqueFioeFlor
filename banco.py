import sqlite3
try:
    # conexao = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     passwd="rafa123",
    #     database="fioeflor"
    # )
    conexao= sqlite3.connect('fioeflor.db')
    cursor = conexao.cursor()
    print("Conectado ao banco")
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
    conexao.commit()
except Exception as erro:
    print('erro', erro)
    exit()