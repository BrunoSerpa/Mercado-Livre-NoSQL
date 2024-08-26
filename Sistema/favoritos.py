import os
from busca import buscarProduto, buscarPorId
from validacoes import obterEntrada
from formatacao import formatacaoProduto, formatarSeparador1

def adicionarFavorito(favoritos=set()):
    produto = None
    while not produto:
        achouProduto = buscarProduto(input('Insira o nome do produto desejado: '), 'nome', True, True)
        if not achouProduto:
            if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return favoritos
        elif isinstance(achouProduto, list):
            id = obterEntrada("Insira o id do produto desejado: ", "validarId", "Id Inválido. Certifique-se de inserir o mesmo id mostrado.")
            produto = buscarProduto(id)
            if not produto:
                if input("Deseja procurar novamente? (S/N)\n").upper() != 'S': return favoritos
        else: produto = achouProduto
    if produto.id in favoritos: print("Este produto já está favoritado!")
    else:
        favoritos.add(produto.id)
        print("Produto favoritado com sucesso")
    return favoritos


def removerFavorito(favoritos=set()):
    os.system('cls')
    for i, idFavorito in enumerate(favoritos):
        favorito = buscarPorId("produtos", idFavorito)
        if not favorito:
            print(f"Produto com id {idFavorito} não encontrado.")
            continue
        vendedor = buscarPorId("vendedores", favorito.id_vendedor)
        print(f'{i + 1}º Favorito:')
        formatarSeparador1()
        formatacaoProduto(favorito, vendedor)
        formatarSeparador1()
    posicao = obterEntrada("Insira a posição do favorito: ", "validarNumero", "Posição inválida. Deve conter apenas dígitos numéricos.") - 1
    if posicao < len(favoritos) and posicao >= 0:
        favorito_remover = list(favoritos)[posicao]
        favoritos.remove(favorito_remover)
        print("Favorito removido com sucesso")
    else: print("A posição fornecida não corresponde a nenhum favorito!")
    return favoritos

    if posicao < len(favoritos) and posicao >= 0:
        favorito_remover = list(favoritos)[posicao]
        favoritos.remove(favorito_remover)
        print("Favorito removido com sucesso")
    else: print("A posição fornecida não corresponde a nenhum favorito!")
    return favoritos

def gerenciarFavoritos(favoritos=set()):
    print("Favoritos Atuais:")
    temFavoritos = len(favoritos) > 0
    if not temFavoritos: print("Nenhum Favorito cadastrado!")
    for i, idFavorito in enumerate(favoritos):
        favorito = buscarPorId("produtos", idFavorito)
        if favorito:
            vendedor = buscarPorId("vendedores", favorito.id_vendedor)
            print(f'{i + 1}º Favorito:')
            print("--------------------------------")
            formatacaoProduto(favorito, vendedor)
            print("--------------------------------")
        else:
            favoritos.remove(idFavorito)
            continue
    print("================================")
    print('O que deseja fazer com os favoritos?')
    print("--------------------------------")
    print('1 - Adicionar um produto')
    if temFavoritos: print('2 - Remover um produto')
    print("--------------------------------")
    print('0 - Voltar')
    print("================================") 
   
    opcao = obterEntrada("Insira a opção desejada: ", "validarNumero", "Opção inválida. Deve conter apenas dígitos numéricos.")
    if opcao == "1": favoritos = adicionarFavorito(favoritos)
    elif opcao == "2" and temFavoritos: favoritos = removerFavorito(favoritos)
    elif opcao != "0": print('Comando incorreto! :(')
    return favoritos