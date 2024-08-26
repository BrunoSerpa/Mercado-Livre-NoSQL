from validacoes import obterEntrada
from formatacao import formatacaoEndereco, formatarSeparador3, formatarSeparador1
from conexaoCassandra import cadastrarRegistro, atualizarRegistro, deletarRegistro
from uuid import uuid4
import os
from busca import buscarPorId


def obterEndereco():
    cep = obterEntrada("Insira o CEP: ", "validarCEP", "CEP inválido. Deve conter 8 dígitos numéricos.")
    pais = obterEntrada("Insira o país: ", "validarNaoVazio", "País não pode estar em branco.")
    estado = obterEntrada("Insira o estado: ", "validarNaoVazio", "Estado não pode estar em branco.")
    cidade = obterEntrada("Insira a cidade: ", "validarNaoVazio", "Cidade não pode estar em branco.")
    bairro = obterEntrada("Insira o bairro: ", "validarNaoVazio", "Bairro não pode estar em branco.")
    rua = obterEntrada("Insira a rua: ", "validarNaoVazio", "Rua não pode estar em branco.")
    numero = obterEntrada("Insira o número: ", "validarNumero", "Número inválido. Deve conter apenas dígitos numéricos.")
    descricao = obterEntrada("Insira a descrição: ", "validarNaoVazio", "Descrição não pode estar em branco.")
    endereco = [cep, pais, estado, cidade, bairro, rua, numero, descricao]
    return endereco


def cadastrarEnderecos(sessao):
    enderecos = set()
    while True:
        idEndereco = cadastrarEndereco(sessao)
        enderecos.add(idEndereco)
        if input("Deseja cadastrar mais algum endereço? (S/N)\n").upper() != 'S': break
    return enderecos
def cadastrarEndereco(sessao):
    tiposDados = ["cep", "pais", "estado", "cidade", "bairro", "rua", "numero", "descricao"]
    endereco = obterEndereco()
    idEndereco = uuid4()
    if cadastrarRegistro(sessao, "enderecos", tiposDados, endereco, idEndereco):
        print("Endereco cadastrado com sucesso")
        return idEndereco

def editarEndereco(sessao, enderecos=set()):
    os.system('cls')
    for i, idEndereco in enumerate(enderecos):
        print(f'{i + 1}º Endereço:')
        formatarSeparador1()
        endereco = buscarPorId("enderecos", idEndereco)
        formatacaoEndereco(endereco)
        formatarSeparador1()
    posicao = obterEntrada("Insira a posição do endereço a ser editado: ", "validarNumero", "Posição inválida. Deve conter apenas dígitos numéricos.") - 1
    if posicao < len(enderecos) and posicao >= 0:
        endereco_editar = list(enderecos)[posicao]
        tiposDados = ["cep", "pais", "estado", "cidade", "bairro", "rua", "numero", "descricao"]
        novo_endereco = obterEndereco()
        if atualizarRegistro(sessao, "enderecos", tiposDados, novo_endereco, endereco_editar): print("Endereco atualizado com sucesso")
    else: print("A posição fornecida não corresponde a nenhum endereço!")


def excluirEndereco(sessao, enderecos=set()):
    os.system('cls')
    for i, idEndereco in enumerate(enderecos):
        print(f'{i + 1}º Endereço:')
        formatarSeparador1()
        endereco = buscarPorId("enderecos", idEndereco)
        formatacaoEndereco(endereco)
        formatarSeparador1()
    posicao = obterEntrada("Insira a posição do endereço: ", "validarNumero", "Posição inválida. Deve conter apenas dígitos numéricos.") - 1
    if posicao < len(enderecos) and posicao >= 0:
        endereco_excluir = list(enderecos)[posicao]
        if deletarRegistro(sessao, "enderecos", endereco_excluir):
            enderecos.remove(endereco_excluir)
            print("Endereco excluído com sucesso")
    else: print("A posição fornecida não corresponde a nenhum endereço!")


def gerenciarEnderecos(sessao, enderecos=set()):
    print("Endereços Atuais:")
    temEnderecos = len(enderecos) > 0
    if not temEnderecos: print("Nenhum endereço cadastrado!")
    else:
        for i, idEndereco in enumerate(enderecos):
            print(f'{i + 1}º Endereço:')
            formatarSeparador1()
            endereco = buscarPorId("enderecos", idEndereco)
            formatacaoEndereco(endereco)
            formatarSeparador1()

    formatarSeparador3()
    print('O que deseja fazer com os endereços?')
    formatarSeparador1()
    print('1 - Criar um novo endereço')
    if temEnderecos:
        print('2 - Editar um endereço existente')
        print('3 - Deletar um endereço existente')
    formatarSeparador1()
    print('0 - Voltar')
    formatarSeparador3()

    opcao = obterEntrada("Insira a opção desejada: ", "validarNumero", "Opção inválida. Deve conter apenas dígitos numéricos.")
    if opcao == "1": enderecos.add(cadastrarEndereco(sessao))
    elif opcao == "2" and temEnderecos: editarEndereco(enderecos)
    elif opcao == "3" and temEnderecos: enderecos = excluirEndereco(sessao, enderecos)
    elif opcao != "0": print('Opção inválida.')
    return enderecos
