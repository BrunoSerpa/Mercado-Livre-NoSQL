from usuario import cadastrarUsuario, atualizarUsuario, listarUsuario, deletarUsuario
from vendedor import cadastrarVendedor, atualizarVendedor, listarVendedor, deletarVendedor
from produtos import cadastrarProduto, atualizarProduto, listarProduto, deletarProduto
from compras import fazerCompra, listarVendas, listarCompras
from validacoes import validarNaoVazio
import os

def exibirMenu(opcoes, titulo="Menu"):
    while True:
        print("================================")
        print(f"{titulo}")
        print("--------------------------------")
        for i, opcao in enumerate(opcoes, start=1): print(f"{i} - {opcao['descricao']}")
        print("--------------------------------")
        print("0 - Voltar")
        print("================================")
        opcao = input("Insira uma opção: ")
        if not validarNaoVazio(opcao):
            os.system('cls')
            print("Insira uma das opções!")
            continue
        if opcao == "0": break
        try:
            opcaoIndex = int(opcao) - 1
            if 0 <= opcaoIndex < len(opcoes):
                os.system('cls')
                opcoes[opcaoIndex]['acao']()
            else: print("Opção inválida!")
        except ValueError: print("Opção inválida!")
def menuUsuario():
    opcoes = [
        {"descricao": "Cadastar usuario", "acao": cadastrarUsuario},
        {"descricao": "Listar usuarios", "acao": listarUsuario},
        {"descricao": "Atualizar usuario", "acao": atualizarUsuario},
        {"descricao": "Deletar usuario", "acao": deletarUsuario}
    ]
    exibirMenu(opcoes, "Gerenciar Usuários")
def menuVendedor():
    opcoes = [
        {"descricao": "Cadastar vendedor", "acao": cadastrarVendedor},
        {"descricao": "Listar vendedores", "acao": listarVendedor},
        {"descricao": "Atualizar vendedor", "acao": atualizarVendedor},
        {"descricao": "Deletar vendedor", "acao": deletarVendedor}
    ]
    exibirMenu(opcoes, "Gerenciar Vendedores")

def menuProduto():
    opcoes = [
        {"descricao": "Cadastar produto", "acao": cadastrarProduto},
        {"descricao": "Listar produtos", "acao": listarProduto},
        {"descricao": "Atualizar produto", "acao": atualizarProduto},
        {"descricao": "Deletar produto", "acao": deletarProduto}
    ]
    exibirMenu(opcoes, "Gerenciar Produtos")
def menuCompra():
    opcoes = [
        {"descricao": "Cadastar compra", "acao": fazerCompra},
        {"descricao": "Listar compras", "acao": listarCompras},
        {"descricao": "Listar vendas", "acao": listarVendas}
    ]
    exibirMenu(opcoes, "Gerenciar Compras")

def home():
    opcoes = [
        {"descricao": "Gerenciar Usuarios", "acao": menuUsuario},
        {"descricao": "Gerenciar Vendedores", "acao": menuVendedor},
        {"descricao": "Gerenciar Produtos", "acao": menuProduto},
        {"descricao": "Gerenciar Compras", "acao": menuCompra}
    ]
    exibirMenu(opcoes, "Menu Principal")

if __name__ == "__main__": home()

"""
Pedro Augusto
81529627087
pedro@augusto.com
12997206478
12226660
Brasil
SP
São José dos Campos
Campos de São José
Rua Álvaro Pinheiro Mendonça
12
Casa
S
12248200
Brasil
SP
São José dos Campos
Jardim Santa Inês I
Avenida Professor Milton Santos
40
Loja
N

Pietra Augusta
97453745000148
pietra@augusta.com
2832443280
12211810
Brasil
SP
São José dos Campos
Santana
Rua Manoel Ramos Machado
32
Loja
N
S
Carregar do Iphone
70.00
S
Carregar de Xiaomi
30.00
S
J4 PLUS
760.00
N
"""