from conexaoCassandra import conectar, cadastrarRegistro, atualizarRegistro, deletarRegistro
import os
from validacoes import obterEntrada
from endereco import cadastrarEnderecos, gerenciarEnderecos
from produtos import cadastrarProdutos, gerenciarProdutos
from uuid import uuid4
from busca import buscarVendedor
from formatacao import formatacaoVendedor

sessao = conectar()

def cadastrarVendedor():
    os.system('cls')
    print("Cadastrando um vendedor...")
    nome = obterEntrada("Insira o nome do vendedor: ", "validarNaoVazio", "Nome não pode estar em branco.")
    cnpj = obterEntrada("Insira o CNPJ do vendedor: ", "validarCNPJ", "CNPJ inválido. Deve conter 14 dígitos numéricos.")
    email = obterEntrada("Insira o email do vendedor: ", "validarEmail", "Email inválido. Certifique-se de que contém '@' e '.'.")
    telefone = obterEntrada("Insira o telefone do vendedor: ", "validarTelefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
    idVendedor = uuid4()
    enderecos = cadastrarEnderecos(sessao)
    produtos = cadastrarProdutos(idVendedor) if input("Deseja cadastrar produtos? (S/N)\n").upper() == "S" else set()
    tiposDados = ["nome_vendedor", "cnpj", "email_vendedor", "telefone_vendedor", "enderecos", "produtos", "vendas"]
    novoVendedor = [nome, cnpj, email, telefone, enderecos, produtos, set()]
    if cadastrarRegistro(sessao, "vendedores", tiposDados, novoVendedor, idVendedor): print("Vendedor cadastrado com sucesso!")

def listarVendedor():
    os.system('cls')
    print("Listando vendedores...")
    try:
        if input("Deseja procurar um vendedor específico? (S/N)\n").upper() == 'S':
            while True:
                nomeVendedor = input('Insira o nome do vendedor desejado: ')
                achouVendedor = buscarVendedor(nomeVendedor, 'nome')
                if not achouVendedor:
                    if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                break   
        else:
            print('Vendedores Existentes:')
            buscarVendedor('', 'nome')
    except Exception as e:
        print(f"Erro ao listar vendedores: {e}")
        input("Insira qualquer coisa para continuar...")

def atualizarVendedor():
    os.system('cls')
    print("Editando vendedor...")
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
    while True:
        formatacaoVendedor(vendedor)
        print("================================")
        print("Que tipo de dado deseja mudar?")
        print("--------------------------------")
        print("1 - Nome")
        print("2 - CNPJ")
        print("3 - Email")
        print("4 - Telefone")
        print("5 - Endereços")
        print("6 - Produtos")
        print("--------------------------------")
        print("0 - Sair")
        print("================================")
        opcao = obterEntrada("Insira a opção desejada: ", "validarNumero", "Opção inválida. Deve conter apenas dígitos numéricos.")
        if opcao == "0": break
        elif opcao == "1":    
            novoNome = obterEntrada("Insira o novo nome do usuário: ", "validarNaoVazio", "Nome não pode estar em branco.")
            atualizarRegistro(sessao, "vendedores", "nome_vendedor", novoNome, vendedor.id)
        elif opcao == "2":
            novoCnpj = obterEntrada("Insira o novo CNPJ do vendedor: ", "validarCNPJ", "CNPJ inválido. Deve conter 14 dígitos numéricos.")
            atualizarRegistro(sessao, "vendedores", "cnpj", novoCnpj, vendedor.id)
        elif opcao == "3":
            novoEmail = obterEntrada("Insira o novo email do vendedor: ", "validarEmail", "Email inválido. Certifique-se de que contém '@' e '.'.")
            atualizarRegistro(sessao, "vendedores", "email_vendedor", novoEmail, vendedor.id)
        elif opcao == "4":
            novoTelefone = obterEntrada("Insira o telefone do vendedor: ", "validarTelefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            atualizarRegistro(sessao, "vendedores", "telefone_vendedor", novoTelefone, vendedor.id)
        elif opcao == "5":
            novosEnderecos = gerenciarEnderecos(sessao, enderecos=vendedor.enderecos)
            atualizarRegistro(sessao, "vendedores", "enderecos", novosEnderecos, vendedor.id)
        elif opcao == "6":
            novosProdutos = gerenciarProdutos(sessao, produtos=vendedor.produtos)
            atualizarRegistro(sessao, "vendedores", "produtos", novosProdutos, vendedor.id)
        else: print("Opção inválida. Deve ser uma opção existente")
        usuario = buscarVendedor(id)

def deletarVendedor():
    os.system('cls')
    print("Deletando vendedor...")
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
    for produto in vendedor.produto:
        if not deletarRegistro(sessao, "produtos", produto): return
    if not deletarRegistro(sessao, "vendedores", vendedor.id): return
    print('Vendedor excluido com sucesso!')