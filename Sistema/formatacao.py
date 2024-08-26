def formatarSeparador1() -> None:
    print("-----------------------------------------------")

def formatarSeparador2() -> None:
    print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def formatarSeparador3() -> None:
    print("===============================================")

def formatarCep(cep: str) -> str:
    if len(cep) == 8: return f'{cep[0:5]}-{cep[5:8]}'
    return cep

def formatarTelefone(telefone: str) -> str:
    if len(telefone) == 8: return f'{telefone[0:4]}-{telefone[4:8]}'
    elif len(telefone) == 9: return f'{telefone[0:5]}-{telefone[5:9]}'
    elif len(telefone) == 10: return f'({telefone[0:2]}) {telefone[2:6]}-{telefone[6:10]}'
    elif len(telefone) == 11: return f'({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}'
    return telefone

def formatarCpf(cpf: str) -> str:
    if len(cpf) == 11: return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    return cpf

def formatarCnpj(cnpj: str) -> str:
    if len(cnpj) == 14: return f'{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    return cnpj

def formatacaoEndereco(endereco, comCodigo: bool = False) -> None:
    if comCodigo: print(f'ID: {endereco.id}')
    print(f'{endereco.rua}, {endereco.numero} ({endereco.descricao}) - {endereco.bairro}')
    print(f'CEP: {formatarCep(endereco.cep)}')
    print(f'{endereco.cidade} - {endereco.estado} ({endereco.pais})')

def formatacaoProduto(produto, vendedor=None, comCodigo: bool = False) -> None:
    if comCodigo: print(f'ID: {produto.id}')
    print(f'Produto: {produto.nome_produto}')
    print(f'Valor: R${produto.valor_produto:.2f}')
    if vendedor:
        formatarSeparador1()
        print(f"Vendedor: {vendedor.nome_vendedor}")
        print(f"CNPJ: {formatarCnpj(vendedor.cnpj)}")
        formatarSeparador1()

def formatacaoVendedor(vendedor, enderecos=[], produtos=[], compras=[], comCodigo: bool = False) -> None:
    if comCodigo: print(f"ID: {vendedor.id}")
    print(f"Nome: {vendedor.nome_vendedor}")
    print(f"CNPJ: {formatarCnpj(vendedor.cnpj)}")
    print(f"Telefone: {formatarTelefone(vendedor.telefone_vendedor)}")
    print(f"Email: {vendedor.email_vendedor}")
    for endereco in enderecos:
        formatarSeparador1()
        formatacaoEndereco(endereco)
    for produto in produtos:
        formatarSeparador1()
        formatacaoProduto(produto)
    for compra in compras:
        formatarSeparador1()
        formatacaoCompras(compra, cliente=compra.cliente, enderecoCliente=compra.enderecoCliente, enderecoVendedor=compra.enderecoVendedor, produtos=compra.produtos)
    if len(enderecos) > 0 or len(produtos) > 0 or len(compras) > 0:
        formatarSeparador1()

def formatacaoUsuario(usuario, enderecos=[], favoritos=[], compras=[], comCodigo: bool = False) -> None:
    if comCodigo: print(f"ID: {usuario.id}")
    print(f"Nome: {usuario.nome_usuario}")
    print(f"CPF: {formatarCpf(usuario.cpf)}")
    print(f"Telefone: {formatarTelefone(usuario.telefone_usuario)}")
    print(f"Email: {usuario.email_usuario}")
    for endereco in enderecos:
        formatarSeparador1()
        formatacaoEndereco(endereco)
    for favorito in favoritos:
        formatarSeparador1()
        formatacaoProduto(favorito.produto, vendedor=favorito.vendedor)
    for compra in compras:
        formatarSeparador1()
        formatacaoCompras(compra, enderecoCliente=compra.enderecoCliente, vendedor=compra.vendedor, enderecoVendedor=compra.enderecoVendedor, produtos=compra.produtos)
    if len(enderecos) > 0 or len(favoritos) > 0 or len(compras) > 0: formatarSeparador1()

def formatacaoCompras(compra, cliente=None, enderecoCliente=None, vendedor=None, enderecoVendedor=None, produtos=[], comCodigo: bool = False) -> None:
    print(f'Data da Compra: {compra.data_compra}')
    if cliente:
        formatarSeparador2()
        print("Cliente:")
        if comCodigo: print(f"ID: {cliente.id}")
        print(f"Nome: {cliente.nome_usuario}")
        print(f"CPF: {formatarCpf(cliente.cpf)}")
        if enderecoCliente:
            print("Endereço:")
            formatarSeparador1()
            formatacaoEndereco(enderecoCliente)
            formatarSeparador1()
        formatarSeparador2()
    if vendedor:
        formatarSeparador2()
        print("Vendedor:")
        if comCodigo: print(f"ID: {vendedor.id}")
        print(f"Nome: {vendedor.nome_vendedor}")
        print(f"CNPJ: {formatarCnpj(vendedor.cnpj)}")
        if enderecoVendedor:
            print("Endereço:")
            formatarSeparador1()
            formatacaoEndereco(enderecoVendedor)
            formatarSeparador1()
        formatarSeparador2()
    formatarSeparador2()
    print("Produtos:")
    for produto in produtos:
        formatarSeparador1()
        formatacaoProduto(produto)
    formatarSeparador1()
    formatarSeparador2()
    print("Total:", compra.valor_total)