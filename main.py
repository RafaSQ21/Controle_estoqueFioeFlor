from banco import *
cursor.execute("UPDATE caixa SET tipo='ENTRADA' WHERE tipo='Entrada'")
conexao.commit()
def listar_produtos():
    cursor.execute("SELECT * FROM estoque")
    produtos = cursor.fetchall()
    print('\nID | Modelo | Tamanho | Fornecedor | Quantidade | Preço | Preço Custo')
    print('-' * 90)
    for produto in produtos:
        print(f'{produto[0]} | {produto[1]} | {produto[2]} | {produto[3]} | {produto[4]} | R$ {produto[5]:.2f} | R$ {produto[6]:.2f}')

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
    ''',
                   (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo))
    conexao.commit()
    print("Produto inserido com sucesso!")

# função cliente
def cadastrar_cliente():
    nome= input("Nome cliente: ")
    sobrenome= input("Sobrenome: ")
    endereco= input('Endereço')
    cursor = conexao.cursor()
    cursor.execute('''
    insert into clientes
    (nome, sobrenome, endereco)
    values (?, ?, ?)
    ''', (nome, sobrenome, endereco))
    conexao.commit()
    print('Cliente inserido com sucesso!')

def listar_clientes():
    cursor.execute("select * from clientes")
    clientes = cursor.fetchall()

    print('ID | Nome | Sobrenome | Endereço')
    print('-' * 60)

    for cliente in clientes:
        print(f'{cliente[0]} | {cliente[1]} | {cliente[2]} | {cliente[3]}')

def excluir_cliente():
    cliente_id = int(input("Cliente ID: "))
    cursor.execute("DELETE FROM clientes WHERE id = ?",(cliente_id,))
    conexao.commit()
    print('Cliente excluido com sucesso!')

#função fornecedor
def cadastrar_fornecedor():
    nome = input("Nome fornecedor: ")
    cursor = conexao.cursor()
    cursor.execute('''
    insert into fornecedor(nome)
    values (?)
    ''', (nome,))
    conexao.commit()
    print('Fornecedor inserido com sucesso!')


def listar_fornecedor():
    cursor.execute("SELECT * FROM fornecedor")
    forenecedor = cursor.fetchall()
    print('\nID | Nome')
    print('-' * 70)
    for fornecedor in forenecedor:
        print(f'{fornecedor[0]} | {fornecedor[1]}')


def excluir_fornecedor():
    fornecedor_id = int(input("Fornecedor ID: "))
    cursor.execute("DELETE FROM fornecedor WHERE id = ?", (fornecedor_id,))
    conexao.commit()
    print('Fornecedor excluido com sucesso!')

def registrar_venda():
    produto_id = int(input("ID do Produto: "))
    quantidade = int(input("Quantidade vendida: "))

    cursor = conexao.cursor()
    cursor.execute('''
    select quantidade, preco
    from estoque
    where id = ?
    ''', (produto_id,))

    produto = cursor.fetchone()

    if produto is None:
        print ('Produto não encontrado')
        return
    estoque_atual = produto[0]
    preco = produto[1]

    if quantidade > estoque_atual:
        print('Estoque Insuficiente!')
        return
    total = preco * quantidade
    cursor.execute('''
    UPDATE estoque
    SET quantidade = quantidade - ?
    WHERE id = ?
    ''', (quantidade, produto_id))

    cursor.execute('''
    insert into Caixa
    (produto_id, tipo, quantidade, valor_total, data_movimentacao)
    values (?, 'ENTRADA', ?, ?, date('now'))
    ''', (produto_id, quantidade, total))
    conexao.commit()
    print(f'Venda registrada! Total: R$ {total:.2f}')

    #ENTRADA MERCADORIA
def entrada_mercadoria():
    produto_id = int(input("ID do Produto: "))
    quantidade = int(input("Quantidade recebida: "))
    cursor = conexao.cursor()

    cursor.execute('''
    update estoque
    set quantidade = quantidade + ?
    where id = ?
    ''', (quantidade, produto_id))
    conexao.commit()
    print('Mercadoria adcionada ao estoque!')

    #RETIRAR DINHEIRO DO CAIXA
def retirar_caixa():
    descricao = input("Descricao: ")
    valor = float(input("Valor: R$ "))
    cursor = conexao.cursor()

    cursor.execute('''
    INSERT INTO caixa
    (produto_id, tipo, quantidade, valor_total, data_movimentacao)
    values (null, 'SAIDA',0,?,date('now'))
    ''', (valor,))
    conexao.commit()
    print('Caixa retirada!')

    #VISUALIZAR CAIXA
def visualizar_caixa():
    cursor = conexao.cursor()
    cursor.execute('select tipo, valor_total from caixa')
    print(cursor.fetchall())
    cursor.execute('''
    select
        c.id,
        e.modelo,
        e.preco,
        c.quantidade,
        c.valor_total,
        c.tipo,
        c.data_movimentacao
    from caixa c
    left join estoque e
        on c.produto_id = e.id
         ''')
    registros = cursor.fetchall()
    print('\n===== CAIXA =====')
    for r in registros:
        print(
            f'id:{r[0]} | '
            f'Produto:{r[1]} | '
            f'Preço unit.:{r[2]:.2f} | '
            f'Quantidade:{r[3]} | '
            f'Valor total:{r[4]:.2f} | '
            f'{r[5]} | '
            f'{r[6]}'
        )
    cursor.execute('''
    select
        sum(case when upper(tipo)='ENTRADA'
            then valor_total else 0 end),
        sum(case when upper(tipo)='SAIDA'
            then valor_total else 0 end)
    from caixa
    ''')
    resultado= cursor.fetchone()
    entradas =  resultado[0] or 0
    saidas = resultado[1] or 0
    saldo = entradas - saidas

    print('\n===== CAIXA=====')
    print(f'Entradas: R$ {entradas:.2f}')
    print(f'Saidas:   R$ {saidas:.2f}')
    print(f'Saldo:    R$ {saldo:.2f}')

#MENU PRINCIPAL
while True:
    print('\n=== SISTEMA FIO& FLOR ===')
    print('1 - Tabela Estoque')
    print('2 - Tabela Clientes')
    print('3 - Tabela Fornecedor')
    print('4 - Caixa')
    print('5 - sair')

    tabela = input('Escolha uma opção:')
    if tabela == '1':
       while True:
          print('\n===== CONTROLE DE ESTOQUE=====')
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
            print('\n===== CLIENTES ====')
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
            print('\n===== FORNECEDORES ====')
            print('1 - Cadastrar fornecedor')
            print('2 - listar fornecedor' )
            print('3 - excluir fornrcedor')
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
        while True:
            print('\n===== CAIXA ====')
            print('1 - Registrar venda')
            print('2 - Entrada Mercadoria')
            print('3 - Retirar dinheiro')
            print('4 - Visualizar caixa')
            print('5 - Voltar')
            opcao = input('Escolha uma opcao: ')
            if opcao == '1':
                registrar_venda()
            elif opcao == '2':
                entrada_mercadoria()
            elif opcao == '3':
                retirar_caixa()
            elif opcao == '4':
                visualizar_caixa()
            elif opcao == '5':
                break
            else:
               print('opçao invalida!')

    elif tabela == '5':
        print('Sistema encerrado!')
        break
    else:
        print('opção invalida!')

