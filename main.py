from banco import *

def listar_produtos():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM estoque")
    print('/n=== PRODUTOS CADASTRADOS===')
    for produto in cursor.fetchall():
        print(produto)

def cadastrar_produto():
    modelo= input("Modelo: ")
    tamanho = input("Tamanho: ")
    fornecedor_id = int(input("Fornecedor ID: "))
    quantidade = int(input("Quantidade: "))
    preco = float(input('Preço final:'))
    preco_custo = float(input('Preço de custo:'))
    cursor.execute('''
    insert into estoque
    (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo)
    values (?, ?, ?, ?, ?, ?)
    ''', (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo))

    conexao.commit()
    print("Produto inserido com sucesso!")

# função cliente
def cadastrar_cliente():
    nome= input("Nome cliente: ")
    sobrenome= input("Sobrenome: ")
    endereco= input("Endereco: ")
    cursor = conexao.cursor()
    cursor.execute('''
    insert into clientes
    (nome, sobrenome, endereco)
    values (?, ?, ?)
    ''', (nome, sobrenome, endereco))

    conexao.commit()
    print('Cliente inserido com sucesso!')

def listar_clientes():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM clientes")
    print('/n=== CLIENTES CADASTRADOS===')
    for clientes in cursor.fetchall():
        print(clientes)

def excluir_cliente():
    cliente_id = int(input("Cliente ID: "))
    cursor.execute("DELETE FROM clientes WHERE id = ?",(cliente_id,))
    conexao.commit()
    print('Cliente excluido com sucesso!')

def cadastrar_fornecedor():
    nome = input("Nome fornecedor: ")
    cursor = conexao.cursor()
    cursor.execute('''
    insert into fornecedor
    (nome)
    values (?)
    ''', (nome,))
    conexao.commit()
    print('Fornecedor inserido com sucesso!')


def listar_fornecedor():
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM fornecedor")
    print('/n=== FORNECEDORES CADASTRADOS===')
    for fornecedor in cursor.fetchall():
        print(fornecedor)


def excluir_fornecedor():
    fornecedor_id = int(input("Fornecedor ID: "))
    cursor.execute("DELETE FROM fornecedor WHERE id = ?", (fornecedor_id,))
    conexao.commit()
    print('Fornecedor excluido com sucesso!')

#MENU PRINCIPAL
while True:
    print('/n=== SISTEMA FIO& FLOR ===')
    print('1 - Tabela Estoque')
    print('2 - Tabela Clientes')
    print('3 - Tabela Fornecedor')
    print('4 - sair')

    tabela = input('Escolha uma opção:')
    if tabela == '1':
       while True:
          print('/n===== CONTROLE DE ESTOQUE=====')
          print('1 - cadastrar produto')
          print('2 - listar produtos' )
          print('3 - sair')

          opcao = input('Escolha uma opcao: ')
          if opcao == '1':
              cadastrar_produto()
          elif opcao == '2':
               listar_produtos()
          elif opcao == '3':
               break
          else:
              print('opção invalida!')
    elif tabela == '2':
        while True:
            print('/n===== CLIENTES ====')
            print('1 - cadastrar cliente')
            print('2 - listar clientes' )
            print('3 - excluir cliente')
            print('4 - voltar')
            opcao = input('Escolha uma opcao: ')
            if opcao == '1':
                cadastrar_cliente()
            elif opcao == '2':
                listar_clientes()
            elif opcao == '3':
                excluir_cliente()
            elif opcao == '4':
                break
            else:
                print('Opção inválida!')

    elif tabela == '3':
        while True:
            print('/n===== FORNECEDORES ====')
            print('1 - Cadastrar fornecedor')
            print('2 - listar fornecedor' )
            print('3 - excluir fornecedor')
            print('4 - voltar')
            opcao = input('Escolha uma opcao: ')
            if opcao == '1':
                cadastrar_fornecedor()
            elif opcao == '2':
                listar_fornecedor()
            elif opcao == '3':
                excluir_fornecedor()
            elif opcao == '4':
                break
            else:
                print('Opção inválida!')
    elif tabela == '4':
        print('Sistema encerrado!')
        break
    else:
        print('opção invalida!')