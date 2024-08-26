from conexaoCassandra import conectar, cadastrarRegistro, atualizarRegistro, deletarRegistro
import os
from uuid import uuid4
from validacoes import obterEntrada
from busca import buscarUsuario
from formatacao import formatacaoUsuario, formatarSeparador3, formatarSeparador1
from endereco import cadastrarEnderecos, gerenciarEnderecos
from favoritos import gerenciarFavoritos
from compras import fazerCompra

sessao = conectar()

def cadastrarUsuario():
    os.system('cls')
    print("Cadastrando um usuário...")    
    nome = obterEntrada("Insira o nome do usuário: ", "validarNaoVazio", "Nome não pode estar em branco.")
    cpf = obterEntrada("Insira o CPF do usuário: ", "validarCPF", "CPF inválido. Deve conter 11 dígitos numéricos.")
    email = obterEntrada("Insira o email do usuário: ", "validarEmail", "Email inválido. Certifique-se de que contém '@' e '.'.")
    telefone = obterEntrada("Insira o telefone do usuário: ", "validarTelefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
    enderecos = cadastrarEnderecos(sessao)
    tiposDados = ["nome_usuario", "cpf", "email_usuario", "telefone_usuario", "enderecos", "favoritos", "compras"]
    novoUsuario = [nome, cpf, email, telefone, enderecos, set(), set()]
    if cadastrarRegistro(sessao, "usuarios", tiposDados, novoUsuario, uuid4()): print("Usuário cadastrado com sucesso!")

def listarUsuario():
    os.system('cls')
    print("Listando usuários...")
    try:
        if input("Deseja procurar um usuário específico? (S/N)\n").upper() == 'S':
            while True:
                nomeUsuario = input('Insira o nome do usuário desejado: ')
                achouUsuario = buscarUsuario(nomeUsuario, 'nome')
                if not achouUsuario:
                    if input("Deseja procurar novamente? (S/N)\n").upper() == 'S': continue
                break
        else:
            print('Usuários Existentes:')
            buscarUsuario('', 'nome')
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        input("Insira qualquer coisa para continuar...")

def atualizarUsuario():
    os.system('cls')
    print("Editando usuário...")
    usuario = None
    while not usuario:
        achouUsuario = buscarUsuario(input('Insira o nome do usuário desejado: '), 'nome', True)
        if not achouUsuario:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouUsuario, dict):
            id = obterEntrada("Insira o id do usuário desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            usuario = buscarUsuario(id)
            if not usuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: usuario = achouUsuario
    while True:
        formatacaoUsuario(usuario)
        formatarSeparador3()
        print("Que tipo de dado deseja mudar?")
        formatarSeparador1()
        print("1 - Nome")
        print("2 - CPF")
        print("3 - Email")
        print("4 - Telefone")
        print("5 - Endereços")
        print("6 - Produtos favoritos")
        print("7 - Fazer compras")
        formatarSeparador1()
        print("0 - Sair")
        formatarSeparador3()
        opcao = obterEntrada("Insira a opção desejada: ", "validarNumero", "Opção inválida. Deve conter apenas dígitos numéricos.")
        if opcao == "0": break
        elif opcao == "1":
            novoNome = obterEntrada("Insira o novo nome do usuário: ", "validarNaoVazio", "Nome não pode estar em branco.")
            atualizarRegistro(sessao, "usuarios", "nome_usuario", novoNome, usuario.id)
        elif opcao == "2":
            novoCPF = obterEntrada("Insira o novo CPF do usuário: ", "validarCPF", "CPF inválido. Deve conter 11 dígitos numéricos.")
            atualizarRegistro(sessao, "usuarios", "cpf", novoCPF, usuario.id)
        elif opcao == "3":
            novoEmail = obterEntrada("Insira o email do usuário: ", "validarEmail", "Email inválido. Certifique-se de que contém '@' e '.'.")
            atualizarRegistro(sessao, "usuarios", "email_usuario", novoEmail, usuario.id)
        elif opcao == "4":
            """ favoritos, compras) """
            novoTelefone = obterEntrada("Insira o telefone do usuário: ", "validarTelefone", "Telefone inválido. Deve conter apenas dígitos numéricos e ter pelo menos 8 caracteres.")
            atualizarRegistro(sessao, "usuarios", "telefone_usuario", novoTelefone, usuario.id)
        elif opcao == "5":
            novosEnderecos = gerenciarEnderecos(usuario.get("enderecos", []))
            atualizarRegistro(sessao, "usuarios", "enderecos", novosEnderecos, usuario.id)
        elif opcao == "6":
            novosFavoritos = gerenciarFavoritos(usuario.get("favoritos", []))
            atualizarRegistro(sessao, "usuarios", "favoritos", novosFavoritos, usuario.id)
        elif opcao == "7":
            novaCompra = fazerCompra(usuario)
            novasCompras = usuario.compras
            if novaCompra: comprasUsuario.add(novaCompra)
            atualizarRegistro(sessao, "usuarios", "compras", novasCompras, usuario.id)
        else: print("Opção inválida. Deve ser uma opção existente")
        usuario = buscarUsuario(usuario.id)

def deletarUsuario():
    os.system('cls')
    print("Excluindo usuário...")
    usuario = None
    while not usuario:
        achouUsuario = buscarUsuario(input('Insira o nome do usuário desejado: '), 'nome', True)
        if not achouUsuario:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        elif not isinstance(achouUsuario, dict):
            id = obterEntrada("Insira o id do usuário desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            usuario = buscarUsuario(id)
            if not usuario:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return
        else: usuario = achouUsuario
    if deletarRegistro(sessao, "cliente", usuario.id): print("Usuário deletado com sucesso!")