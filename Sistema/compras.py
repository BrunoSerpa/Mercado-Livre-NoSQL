import os
from busca import buscarCompra, buscarUsuario, buscarProduto, buscarVendedor, buscarPorId
from formatacao import formatacaoEndereco, formatacaoProduto
from validacoes import obterEntrada
from datetime import datetime
from uuid import uuid4
from conexaoCassandra import cadastrarRegistro, atualizarRegistro, deletarRegistro

def fazerCompra(sessao, cliente=None):
    os.system('cls')
    print("Fazendo compras...")
    while not cliente:
        achouCliente = buscarUsuario(input('Insira o nome do cliente desejado: '), 'nome', True)
        if not achouCliente:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouCliente, dict):
            id = obterEntrada("Insira o id do usuário desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            cliente = buscarUsuario(id)
            if not cliente:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: cliente = achouCliente

    enderecoCliente = None
    quantEndCli = len(cliente.enderecos)
    if quantEndCli == 0:
        print("Cadastre um endereço no cliente antes de fazer uma compra!")
        return
    elif quantEndCli > 1:
        while not enderecoCliente:
            print("Para onde devemos enviar o produto?")
            for i, idEndereco in enumerate(cliente.enderecos):
                print(f'{i + 1}º Endereço:')
                print("--------------------------------")
                endereco = buscarPorId("enderecos", idEndereco)
                formatacaoEndereco(endereco)
                print("--------------------------------")
            posicao = obterEntrada("Insira a posição do endereço a ser enviado: ", "validarNumero", "Posição inválida. Deve conter apenas dígitos numéricos.") - 1
            if posicao < len(cliente.enderecos) and posicao >= 0: enderecoCliente = list(cliente.enderecos)[posicao]
            else:
                print("A posição fornecida não corresponde a nenhum endereço!")
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
    else: enderecoCliente = list(cliente.enderecos)[0]

    vendedor = None
    while not vendedor:
        achouVendedor = buscarVendedor(input('Insira o nome do vendedor desejado: '), 'nome', True)
        if not achouVendedor:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouVendedor, dict):
            id = obterEntrada("Insira o id do vendedor desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            vendedor = buscarVendedor(id)
            if not vendedor:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: vendedor = achouVendedor

    enderecoVendedor = None
    quantEndVen = len(vendedor.enderecos)
    if quantEndVen == 0:
        print("Cadastre um endereço no vendedor antes de fazer uma compra!")
        return
    elif quantEndVen > 1:
        while not enderecoVendedor:
            print("De onde devemos enviar os produtos?")
            for i, idEndereco in enumerate(vendedor.enderecos):
                print(f'{i + 1}º Endereço:')
                print("--------------------------------")
                endereco = buscarPorId("enderecos", idEndereco)
                formatacaoEndereco(endereco)
                print("--------------------------------")
            posicao = obterEntrada("Insira a posição do endereço a ser retirado: ", "validarNumero", "Posição inválida. Deve conter apenas dígitos numéricos.") - 1
            if posicao < len(vendedor.enderecos) and posicao >= 0: enderecoVendedor = list(vendedor.enderecos)[posicao]
            else:
                print("A posição fornecida não corresponde a nenhum endereço!")
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
    else: enderecoVendedor = list(vendedor.enderecos)[0]

    produtosVendedor = vendedor.produtos
    quantProVen = len(produtosVendedor)
    produtos = set()
    valorTotal = 0
    if quantProVen == 0:
        print("Cadastre um produto no vendedor antes de fazer uma compra!")
        return
    elif quantProVen > 1:
        while quantProVen > len(produtos):
            precos = []
            print("Escolha o produto a ser comprado")
            for i, idProduto in enumerate(produtosVendedor):
                print(f'{i + 1}º produto:')
                print("--------------------------------")
                produto = buscarPorId("produtos", idProduto)
                formatacaoProduto(produto)
                precos.append(produto.valor_produto)
                print("--------------------------------")
            posicao = obterEntrada("Insira a posição do produto a ser comprado: ", "validarNumero", "Posição inválida. Deve conter apenas dígitos numéricos.") - 1
            if posicao < len(produtosVendedor) and posicao >= 0:
                produtoComprado = list(produtosVendedor)[posicao]
                produtos.add(produtoComprado)
                produtosVendedor.remove(produtoComprado)
                valorTotal += precos[posicao]
                if len(produtosVendedor) == 1:
                    if input("Deseja comprar o último produto? (S/N)\n").upper() == 'S':
                        produtoComprado = list(produtosVendedor)[0]
                        produtos.add(produtoComprado)
                        produtosVendedor.remove(produtoComprado)
                        valorTotal += precos[0]
            else:
                print("A posição fornecida não corresponde a nenhum produto!")
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
    else:
        idProduto = list(vendedor.produtos)[0]
        produtos.add(idProduto)
        produto = buscarPorId("produtos", idProduto)
        valorTotal = produto.valor_produto

    tiposDados = ["data_compra", "id_cliente", "endereco_cliente", "id_vendedor", "endereco_vendedor", "produtos", "valor_total"]
    compra = [datetime.utcnow(), cliente.id, enderecoCliente, vendedor.id, enderecoVendedor, list(produtos), valorTotal]
    idCompra = uuid4()
    cliente.compras.add(idCompra)
    vendedor.vendas.add(idCompra)
    vendedor.produtos = set(produtosVendedor)

    if not cadastrarRegistro(sessao, "compras", tiposDados, compra, idCompra): return
    if not atualizarRegistro(sessao, "usuarios", "compras", cliente.compras, cliente.id): return
    if not atualizarRegistro(sessao, "vendedores", "vendas", vendedor.vendas, vendedor.id): return
    if not atualizarRegistro(sessao, "vendedores", "produtos", vendedor.produtos, vendedor.id): return

    print("Compra realizada com sucesso!")

def listarCompras():
    os.system('cls')
    print("Listando compras...")
    if input("Deseja procurar compras de um usuário específico? (S/N)\n").upper() == 'S':
        while True:
            nomeUsuario = input('Insira o nome do usuário desejado: ')
            achouUsuario = buscarCompra(nomeUsuario, 'nome_cliente', True)
            if not achouUsuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Compras Existentes:')
        buscarCompra('', 'nome_cliente', False)

def listarVendas():
    os.system('cls')
    print("Listando vendas...")
    if input("Deseja procurar vendas de um vendedor específico? (S/N)\n").upper() == 'S':
        while True:
            nomeVendedor = input('Insira o nome do vendedor desejado: ')
            achouUsuario = buscarCompra(nomeVendedor, 'nome_vendedor', True)
            if not achouUsuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
            break
    else:
        print('Vendas Existentes:')
        buscarCompra('', 'nome_vendedor', False)

def excluirCompra(sessao, compra=None):
    while not compra:
        achouCompra = buscarCompra(input('Insira o nome do cliente que fez a compra desejada: '), 'nome_cliente', True)
        if not achouCompra:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouCompra, dict):
            id = obterEntrada("Insira o id da compra desejada: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            compra = buscarCompra(id)
        if not compra:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: compra = achouCompra

    cliente = buscarPorId("usuarios", compra.id_cliente)
    cliente.compras.remove(compra.id)

    vendedor = buscarPorId("vendedores", compra.id_vendedor)
    vendedor.vendas.remove(compra.id)
    vendedor.produtos.update(compra.produtos)

    if not deletarRegistro(sessao, "compras", compra.id): return
    if not atualizarRegistro(sessao, "usuarios", "compras", cliente.compras, cliente.id): return
    if not atualizarRegistro(sessao, "vendedores", "vendas", vendedor.vendas, vendedor.id): return
    if not atualizarRegistro(sessao, "vendedores", "produtos", vendedor.produtos, vendedor.id): return

    print("Compra excluída com sucesso!")