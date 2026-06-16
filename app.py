from flask import Flask, render_template, request, redirect
from banco import *
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/produtos')
def produtos():
    cursor.execute('select * from estoque')
    produtos = cursor.fetchall()
    return render_template('produtos.html', produtos=produtos)

@app.route('/clientes')
def clientes():
    cursor.execute('select * from clientes')
    clientes = cursor.fetchall()
    return render_template('clientes.html', clientes=clientes)

@app.route('/incluir_cliente', methods=['POST'])
def incluir_cliente():
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    endereco = request.form['endereco']

    cursor.execute("""
        INSERT INTO clientes (nome, sobrenome, endereco)
        VALUES (?, ?, ?)
    """, (nome, sobrenome, endereco))
    conexao.commit()

    return redirect('/clientes')

@app.route('/fornecedores')
def fornecedores():
    cursor.execute('select * from fornecedor')
    fornecedores = cursor.fetchall()
    return render_template('fornecedores.html', fornecedores=fornecedores)
@app.route('/incluir_fornecedor', methods=['POST'])
def incluir_fornecedor():
    nome = request.form['nome']

    cursor.execute("""
        INSERT INTO fornecedor (nome)
        VALUES (?)
    """, (nome, ))
    conexao.commit()
    return redirect('/fornecedores')

@app.route('/cadastrar_produto', methods=['POST'])
def cadastrar_produto():

    modelo = request.form['modelo']
    tamanho = request.form['tamanho']
    fornecedor_id = int(request.form['fornecedor_id'])
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    preco_custo = float(request.form['preco_custo'])

    cursor.execute('''
    INSERT INTO estoque
    (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo)
    VALUES (?, ?, ?, ?, ?, ?)
    ''',
    (modelo, tamanho, fornecedor_id, quantidade, preco, preco_custo))

    conexao.commit()
    return redirect('/produtos')

@app.route('/excluir/<int:id>', methods=['POST'])
def excluir(id):
    cursor.execute("DELETE FROM estoque WHERE id = ?", (id,))
    conexao.commit()
    return redirect('/produtos')

@app.route('/caixa')
def caixa():
    cursor.execute("""
        SELECT
            c.id,
            e.modelo,
            c.quantidade,
            c.valor_total,
            c.tipo,
            c.data_movimentacao
        FROM caixa c
        LEFT JOIN estoque e
        ON c.produto_id = e.id
        ORDER BY c.id DESC
    """)

    registros = cursor.fetchall()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN tipo='ENTRADA' THEN valor_total ELSE 0 END),
            SUM(CASE WHEN tipo='SAIDA' THEN valor_total ELSE 0 END)
        FROM caixa
    """)

    resultado = cursor.fetchone()
    entradas = resultado[0] or 0
    saidas = resultado[1] or 0
    saldo = entradas - saidas

    return render_template(
        "caixa.html",
        registros=registros,
        entradas=entradas,
        saidas=saidas,
        saldo=saldo
    )

@app.route('/caixa/saida', methods=['POST'])
def caixa_saida():
    descricao = request.form['descricao']
    valor = float(request.form['valor'])

    cursor.execute("""
        INSERT INTO caixa (produto_id, tipo, quantidade, valor_total, data_movimentacao)
        VALUES (NULL, 'SAIDA', 0, ?, date('now'))
    """, (valor,))

    conexao.commit()
    return redirect('/caixa')

@app.route('/vender', methods=['POST'])
def vender():
    produto_id = int(request.form['produto_id'])
    quantidade = int(request.form['quantidade'])

    # pega produto
    cursor.execute("SELECT quantidade, preco FROM estoque WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()

    if not produto:
        return "Produto não encontrado"

    estoque_atual = produto[0]
    preco = produto[1]

    if quantidade > estoque_atual:
        return "Estoque insuficiente"

    # calcula valor total
    valor_total = quantidade * preco

    # baixa estoque
    novo_estoque = estoque_atual - quantidade

    cursor.execute("""
        UPDATE estoque
        SET quantidade = ?
        WHERE id = ?
    """, (novo_estoque, produto_id))

    # registra entrada no caixa
    cursor.execute("""
        INSERT INTO caixa (produto_id, tipo, quantidade, valor_total, data_movimentacao)
        VALUES (?, 'ENTRADA', ?, ?, date('now'))
    """, (produto_id, quantidade, valor_total))

    conexao.commit()

    return redirect('/caixa')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
