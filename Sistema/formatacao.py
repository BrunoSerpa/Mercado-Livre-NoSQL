def formatacaoEndereco(arquivoJson, comCodigo=False):
    if comCodigo: print(f'ID: {arquivoJson.id}')
    print(f'{arquivoJson.rua}, {arquivoJson.numero} ({arquivoJson.descricao}) - {arquivoJson.bairro}')
    print(f'CEP: {formatar_cep(arquivoJson.cep)}')
    print(f'{arquivoJson.cidade} - {arquivoJson.estado} ({arquivoJson.pais})')


def formatacaoProduto(arquivoJson, vendedor=None, comCodigo=False):
    if comCodigo: print(f'ID: {arquivoJson.id}')
    print(f'Produto: {arquivoJson.nome_produto}')
    print(f'Valor: R${arquivoJson.valor_produto:.2f}')
    if vendedor:
        print("-----------------------------------------------")
        print(f"Vendedor: {vendedor.nome_vendedor}")
        print(f"CNPJ: {formatar_cnpj(vendedor.cnpj)}")
        print("-----------------------------------------------")
    
def formatacaoVendedor(arquivoJson, enderecos=[], produtos=[], compras=[], comCodigo=False):
    if comCodigo: print(f"ID: {arquivoJson.id}")
    print(f"Nome: {arquivoJson.nome_vendedor}")
    print(f"CNPJ: {formatar_cnpj(arquivoJson.cnpj)}")
    print(f"Telefone: {formatar_telefone(arquivoJson.telefone_vendedor)}")
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
            produtos=compra.produtos,
            cliente=compra.cliente,
            enderecoCliente=compra.enderecoCliente,
            vendedor=compra.vendedor,
            enderecoVendedor=compra.enderecoVendedor
        )
    if len(enderecos)>0 or len(produtos)>0 or len(compras)>0: print("-----------------------------------------------")

def formatacaoUsuario(arquivoJson, enderecos=[], favoritos=[], compras=[], comCodigo=False):
    if comCodigo: print(f"ID: {arquivoJson.id}")
    print(f"Nome: {arquivoJson.nome_usuario}")
    print(f"CPF: {formatar_cpf(arquivoJson.cpf)}")
    print(f"Telefone: {formatar_telefone(arquivoJson.telefone_usuario)}")
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
            produtos=compra.produtos,
            cliente=compra.cliente,
            enderecoCliente=compra.enderecoCliente,
            vendedor=compra.vendedor,
            enderecoVendedor=compra.enderecoVendedor
        )
    if len(enderecos)>0 or len(favoritos)>0 or len(compras)>0: print("-----------------------------------------------")

def formatacaoCompras(arquivoJson, cliente=None, enderecoCliente=None, vendedor=None, enderecoVendedor=None, produtos=[], comCodigo=False):
    print(f'Data da Compra: {arquivoJson.data_compra}')
    if cliente:
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print("Cliente:")
        if comCodigo: print(f"ID: {cliente.id}")
        print(f"Nome: {cliente.nome_usuario}")
        print(f"CPF: {formatar_cpf(cliente.cpf)}")
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
        print(f"CNPJ: {formatar_cnpj(vendedor.cnpj)}")
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
    print("Total:", arquivoJson.valor_total)

def formatar_telefone(telefone):
    if len(telefone) == 8: return f'{telefone[0:4]}-{telefone[4:8]}'
    elif len(telefone) == 9: return f'{telefone[0:5]}-{telefone[5:9]}'
    elif len(telefone) == 10: return f'({telefone[0:2]}) {telefone[2:6]}-{telefone[6:10]}'
    elif len(telefone) == 11: return f'({telefone[0:2]}) {telefone[2:7]}-{telefone[7:11]}'
    else: return telefone

def formatar_cpf(cpf):
    if len(cpf) == 11: return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    else: return cpf

def formatar_cnpj(cnpj):
    if len(cnpj) == 14: return f'{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    else: return cnpj

def formatar_cep(cep):
    if len(cep) == 8: return f'{cep[0:5]}-{cep[5:8]}'
    else: return cep