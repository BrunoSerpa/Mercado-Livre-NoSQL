def formatacaoEndereco(endereco, comCodigo=False):
    if comCodigo: print(f'ID: {endereco.id}')
    print(f'{endereco.rua}, {endereco.numero} ({endereco.descricao}) - {endereco.bairro}')
    print(f'CEP: {formatarCep(endereco.cep)}')
    print(f'{endereco.cidade} - {endereco.estado} ({endereco.pais})')


def formatacaoProduto(produto, vendedor=None, comCodigo=False):
    if comCodigo: print(f'ID: {produto.id}')
    print(f'Produto: {produto.nome_produto}')
    print(f'Valor: R${produto.valor_produto:.2f}')
    if vendedor:
        print("-----------------------------------------------")
        print(f"Vendedor: {vendedor.nome_vendedor}")
        print(f"CNPJ: {formatarCnpj(vendedor.cnpj)}")
        print("-----------------------------------------------")
    
def formatacaoVendedor(vendedor, enderecos=[], produtos=[], compras=[], comCodigo=False):
    if comCodigo: print(f"ID: {vendedor.id}")
    print(f"Nome: {vendedor.nome_vendedor}")
    print(f"CNPJ: {formatarCnpj(vendedor.cnpj)}")
    print(f"Telefone: {formatarTelefone(vendedor.telefone_vendedor)}")
    for endereco in enderecos:
        print("-----------------------------------------------")
        formatacaoEndereco(endereco)
    for produto in produtos:
        print("-----------------------------------------------")
        formatacaoProduto(produto)
    for compra in compras:
        print("-----------------------------------------------")
        formatacaoCompras(
            compra,
            cliente=compra.cliente,
            enderecoCliente=compra.enderecoCliente,
            enderecoVendedor=compra.enderecoVendedor,
            produtos=compra.produtos,
        )
    if len(enderecos) > 0 or len(produtos) > 0 or len(compras) > 0: print("-----------------------------------------------")

def formatacaoUsuario(usuario, enderecos=[], favoritos=[], compras=[], comCodigo=False):
    if comCodigo: print(f"ID: {usuario.id}")
    print(f"Nome: {usuario.nome_usuario}")
    print(f"CPF: {formatarCpf(usuario.cpf)}")
    print(f"Telefone: {formatarTelefone(usuario.telefone_usuario)}")
    for endereco in enderecos:
        print("-----------------------------------------------")
        formatacaoEndereco(endereco)
    for favorito in favoritos:
        print("-----------------------------------------------")
        formatacaoProduto(
            favorito.produto,
            vendedor=favorito.vendedor
        )
    for compra in compras:
        print("-----------------------------------------------")
        formatacaoCompras(
            compra,
            enderecoCliente=compra.enderecoCliente,
            vendedor=compra.vendedor,
            enderecoVendedor=compra.enderecoVendedor,
            produtos=compra.produtos,
        )
    if len(enderecos) > 0 or len(favoritos) > 0 or len(compras) > 0: print("-----------------------------------------------")

def formatacaoCompras(compra, cliente=None, enderecoCliente=None, vendedor=None, enderecoVendedor=None, produtos=[], comCodigo=False):
    print(f'Data da Compra: {compra.data_compra}')
    if cliente:
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Cliente:")
        if comCodigo: print(f"ID: {cliente.id}")
        print(f"Nome: {cliente.nome_usuario}")
        print(f"CPF: {formatarCpf(cliente.cpf)}")
        if enderecoCliente:
            print("Endereço:")
            print("-----------------------------------------------")
            formatacaoEndereco(enderecoCliente)
            print("-----------------------------------------------")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    if vendedor:
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Vendedor:")
        if comCodigo: print(f"ID: {vendedor.id}")
        print(f"Nome: {vendedor.nome_vendedor}")
        print(f"CNPJ: {formatarCnpj(vendedor.cnpj)}")
        if enderecoVendedor:
            print("Endereço:")
            print("-----------------------------------------------")
            formatacaoEndereco(enderecoVendedor)
            print("-----------------------------------------------")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Produtos:")
    for produto in produtos:
        print("-----------------------------------------------")
        formatacaoProduto(produto)
    print("-----------------------------------------------")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Total:", compra.valor_total)

def formatarTelefone(telefone):
    if len(telefone) == 8: return f'{telefone[0:4]}-{telefone[4:8]}'
    elif len(telefone) == 9: return f'{telefone[0:5]}-{telefone[5:9]}'
    elif len(telefone) == 10: return f'({telefone[0:2]}) {telefone[2:6]}-{telefone[6:10]}'
    elif len(telefone) == 11: return f'({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}'
    else: return telefone

def formatarCpf(cpf):
    if len(cpf) == 11: return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    else: return cpf

def formatarCnpj(cnpj):
    if len(cnpj) == 14: return f'{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    else: return cnpj

def formatarCep(cep):
    if len(cep) == 8: return f'{cep[0:5]}-{cep[5:8]}'
    else: return cep