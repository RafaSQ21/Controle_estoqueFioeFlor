import mysql.connector

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="rafa123",
        database="fioeflor"
    )
    cursor = conexao.cursor()
    print("Conectado ao banco")
except Exception as erro:
    print('erro', erro)
    exit()