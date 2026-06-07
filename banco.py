import mysql.connector

try:
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="rafa123",
        database="fioeflor"
    )
    print("Conectado ao banco")
    modelo= input("Modelo: ")
    tamanho = input("Tamanho: ")
    fornecedor_id = int(input("Fornecedor ID: "))
    quantidade = int(input("Quantidade: "))
    preco = float(input('Preço final:'))
    preco_custo = float(input('Preço de custo:'))
    cursor = conexao.cursor()
    cursor.execute('''
    insert into estoque
    (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo)
    values (%s, %s, %s, %s, %s, %s)
    ''',
                   (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo))
    conexao.commit()
    print("Produto inserido com sucesso!")
except Exception as erro:
    print('erro', erro)

