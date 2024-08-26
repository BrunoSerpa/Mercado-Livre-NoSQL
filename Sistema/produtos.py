from conexaoCassandra import conectar, cadastrarRegistro, atualizarRegistro, deletarRegistro
import os
from busca import buscarVendedor, buscarProduto
from validacoes import obterEntrada
from uuid import uuid4
from formatacao import formatacaoProduto

sessao = conectar()

def cadastrarProdutos(idVendedor):
    produtos = set()
    while True:
        idProduto = cadastrarProduto(idVendedor)
        produtos.add(idProduto)
        if input("Deseja cadastrar mais algum produto? (S/N)\n").upper() != 'S': break
    return produtos

def cadastrarProduto(idVendedor=None):
    atualizaVendedor = idVendedor == None
    if atualizaVendedor: os.system('cls')
    print("Cadastrando produto...")
    while not idVendedor:
        achouVendedor = buscarVendedor(input('Insira o nome do vendedor desejado: '), 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouVendedor, dict):
            id = obterEntrada("Insira o id do vendedor desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            vendedor = buscarVendedor(id)
            if not vendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
            idVendedor =  vendedor.id
        else:
            vendedor = achouVendedor
            idVendedor = achouVendedor.id

    nomeProduto = obterEntrada("Insira o nome do produto: ", "validarNaoVazio", "Nome não pode estar em branco.")
    valorProduto = float(obterEntrada("Insira o valor do produto: R$", "validarFloat", "O valor só pode ser um número."))

    tiposDados = ["nome_produto", "valor_produto", "id_vendedor"]
    produto = [nomeProduto, valorProduto, idVendedor]
    idProduto = uuid4()
    cadastrarRegistro(sessao, "produtos", tiposDados, produto, idProduto)
    if atualizaVendedor:
        vendedor.produtos.update(produto.idProduto)
        atualizarRegistro(sessao, "vendedores", "produtos", vendedor.produtos, vendedor.id)
    return idProduto

def listarProduto():
    os.system('cls')
    print("Listando produtos...")
    try:
        if input("Deseja procurar um produto específico? (S/N)\n").upper() == 'S':
            while True:
                nomeProduto = input('Insira o nome do produto desejado: ')
                achouProduto = buscarProduto(nomeProduto, 'nome', comVendedor=True)
                if not achouProduto:
                    if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                break
        else:
            print('Produtos Existentes:')
            buscarProduto('', 'nome')
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        input("Insira qualquer coisa para continuar...")

def atualizarProduto(idProduto=None):
    os.system('cls')
    produto = None
    if idProduto: produto = buscarProduto(idProduto)
    print("Alterando produto...")
    while not produto:
        achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True, True)
        if not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouProduto, dict):
            id = obterEntrada("Insira o id do produto desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            produto = buscarProduto(id)
            if not produto:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: produto = achouProduto
        
    produto.nome_produto = obterEntrada("Insira o novo nome do produto: ", "validarNaoVazio", "Nome não pode estar em branco.")
    produto.valor_produto = float(obterEntrada("Insira o novo valor do produto: R$", "validarFloat", "O valor só pode ser um número."))

    if not atualizarRegistro(sessao, "produtos", "nome_produto", produto.nome_produto, produto.id): return
    if not atualizarRegistro(sessao, "produtos", "valor_produto", produto.valor_produto, produto.id): return
    
    print("Produto atualizado com sucesso!")

def deletarProduto(idProduto):
    os.system('cls')
    atualizaVendedor = idProduto == None
    produto = None
    if idProduto: produto = buscarProduto(idProduto)
    print("Deletando produto...")
    while not produto:
        achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True, True)
        if not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouProduto, dict):
            id = obterEntrada("Insira o id do produto desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            produto = buscarProduto(id)
            if not produto:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: produto = achouProduto
    if atualizaVendedor:
        vendedor = buscarVendedor(produto.id_vendedor)
        vendedor.produtos.remove(produto.idProduto)
        atualizarRegistro(sessao, "vendedores", "produtos", vendedor.produtos, vendedor.id)
    deletarRegistro(sessao, "produtos", produto.id)

def gerenciarProdutos(produtos):
    print("Produtos Atuais:")
    temProduto = len(favoritos) > 0
    if not temProduto: print("Nenhum produto cadastrado!")
    for i, idProduto in enumerate(produtos):
        produto = buscarPorId("produtos", idProduto)
        print(f'{i + 1}º Produto:')
        print("--------------------------------")
        formatacaoProduto(produto, comCodigo=True)
        print("--------------------------------")
    print("================================")
    print("O que deseja fazer com os produtos?")
    print("--------------------------------")
    print("1 - Criar um novo Produto")
    if temProduto:
        print("2 - Editar um produto existente")
        print("3 - Deletar um produto existente")
    print("--------------------------------")
    print("0 - Voltar")
    print("================================")

    opcao = obterEntrada("Insira a opção desejada: ", "validarNumero", "Opção inválida. Deve conter apenas dígitos numéricos.")

    if opcao == '1':
        vendedor = buscarVendedor(idVendedor, 'id', False)
        if vendedor:
            novoProduto = cadastrarProduto(vendedor)
            if novoProduto: produtos.append(novoProduto)
    elif opcao in ['2', '3'] and temProduto:
        idProduto = obterEntrada("Insira a id do produto desejado: ", "validarId", "Id inválido. Insira o exato id mostrado.")
        if not idProduto in produtos: print("Insira um id existente nos produtos!")
        elif opcao == '2': atualizarProduto(idProduto)
        elif opcao == '3': produtos = deletarProduto(idProduto)
    elif opcao != "0": print('Comando inválido.')
    return produtos