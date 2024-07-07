from conexaoCassandra import conectar
from formatacao import formatacaoUsuario, formatacaoVendedor, formatacaoProduto, formatacaoCompras

sessao = conectar()

def buscarDocumento(query, parametros=None):
    documentos = sessao.execute(query) if parametros is None else sessao.execute(query, parametros)
    documentos = list(documentos)
    return documentos if documentos else None

def buscarPorId(colecao, objectId):
    dado = sessao.execute(f"SELECT * FROM {colecao} WHERE id = %s", [objectId])
    dado = list(dado)
    return dado[0] if dado else None

def buscarUsuario(dadoProcurado, tipoDado=None, comCodigo=False):
    if tipoDado == 'nome':
        query = "SELECT * FROM usuarios WHERE nome_usuario = %s ALLOW FILTERING" if dadoProcurado else "SELECT * FROM usuarios"
        listaUsuarios = buscarDocumento(query, [dadoProcurado] if dadoProcurado else None)
        if not listaUsuarios:
            print("Nenhum usuário encontrado!")
            return False
        for usuario in listaUsuarios:
            print("===========================================")
            enderecos = []
            if usuario.enderecos is not None:
                for endereco in usuario.enderecos:
                    enderecoBuscado = buscarPorId("enderecos", endereco)
                    if enderecoBuscado: enderecos.append(enderecoBuscado)
            favoritos = []
            if usuario.favoritos is not None:
                for favorito in usuario.favoritos:
                    produtoEscolhido = buscarPorId("produtos", favorito)
                    vendedorProduto = buscarPorId("vendedores", produtoEscolhido.id_vendedor) if produtoEscolhido else None
                    if produtoEscolhido:
                        favoritos.append({
                            "produto": produtoEscolhido,
                            "vendedor": vendedorProduto
                        })
            compras = []
            if usuario.compras is not None:
                for compra in usuario.compras:
                    compraFeita = buscarPorId("compras", compra)
                    if compraFeita:
                        vendedor = buscarPorId("vendedores", compraFeita.id_vendedor)
                        enderecoVendedor = buscarPorId("enderecos", compraFeita.endereco_vendedor)
                        produtosCompra = [buscarPorId("produtos", produto_id) for produto_id in compraFeita.produtos]
                        compras.append({
                            'compra': compraFeita,
                            'vendedor': vendedor,
                            'enderecoVendedor': enderecoVendedor,
                            'produtos': produtosCompra
                        })
            formatacaoUsuario(usuario, enderecos, favoritos, compras, comCodigo)
        print("===========================================")
        return listaUsuarios if len(listaUsuarios) > 1 else (listaUsuarios[0] if listaUsuarios else None)
    return buscarPorId("usuarios", dadoProcurado)

def buscarVendedor(dadoProcurado, tipoDado=None, comCodigo=False):
    if tipoDado == 'nome':
        query = "SELECT * FROM vendedores WHERE nome_vendedor = %s ALLOW FILTERING" if dadoProcurado else "SELECT * FROM vendedores"
        listaVendedores = buscarDocumento(query, [dadoProcurado] if dadoProcurado else None)
        if not listaVendedores:
            print("Nenhum vendedor encontrado!")
            return False
        for vendedor in listaVendedores:
            print("===========================================")
            enderecos = []
            if vendedor.enderecos is not None:
                for endereco in vendedor.enderecos:
                    enderecoBuscado = buscarPorId("enderecos", endereco)
                    if enderecoBuscado: enderecos.append(enderecoBuscado)
            produtos = []
            if vendedor.produtos is not None:
                for favorito in vendedor.produtos:
                    produtoVendido = buscarPorId("produtos", favorito)
                    if produtoVendido: produtos.append(produtoVendido)
            vendas = []
            if vendedor.vendas is not None:
                for venda in vendedor.vendas:
                    vendaFeita = buscarPorId("vendas", venda)
                    if vendaFeita:
                        cliente = buscarPorId("usuarios", vendaFeita.id_cliente)
                        enderecoCliente = buscarPorId("enderecos", vendaFeita.endereco_cliente)
                        produtosvenda = [buscarPorId("produtos", produto_id) for produto_id in vendaFeita.produtos]
                        vendas.append({
                            'venda': vendaFeita,
                            'cliente': cliente,
                            'enderecoCliente': enderecoCliente,
                            'produtos': produtosvenda
                        })
            formatacaoVendedor(vendedor, enderecos, produtos, vendas, comCodigo)
        print("===========================================")
        return listaVendedores if len(listaVendedores) > 1 else listaVendedores[0]
    return buscarPorId("usuarios", dadoProcurado)

def buscarProduto(dadoProcurado, tipoDado=None, comCodigo=False, comVendedor=False):
    if tipoDado == 'nome':
        query = "SELECT * FROM produtos WHERE nome_produto = %s ALLOW FILTERING" if dadoProcurado else "SELECT * FROM produtos"
        listaProdutos = buscarDocumento(query, [dadoProcurado] if dadoProcurado else None)
        if not listaProdutos:
            print("Nenhum produto encontrado!")
            return False
        if comVendedor:
            for produto in listaProdutos:
                print("===========================================")
                vendedor = buscarPorId("vendedores", produto.id_vendedor)
                formatacaoProduto(produto, vendedor, comCodigo)
            print("===========================================")
        else:
            for produto in listaProdutos:
                print("===========================================")
                formatacaoProduto(produto, comCodigo=comCodigo)
        return listaProdutos if len(listaProdutos) > 1 else listaProdutos[0]
    return buscarPorId("produtos", dadoProcurado)

def buscarCompra(dadoProcurado, tipoDado=None, comCodigo=False):
    if tipoDado == 'nome_cliente': query = "SELECT * FROM compras WHERE nome_cliente = %s ALLOW FILTERING"
    elif tipoDado == 'id_cliente': query = "SELECT * FROM compras WHERE id_cliente = %s ALLOW FILTERING"
    elif tipoDado == 'nome_vendedor': query = "SELECT * FROM compras WHERE nome_vendedor = %s ALLOW FILTERING"
    elif tipoDado == 'id_vendedor': query = "SELECT * FROM compras WHERE id_vendedor = %s ALLOW FILTERING"
    else: return buscarPorId("compras", dadoProcurado)
    
    if dadoProcurado == '' or None:
        query = "SELECT * FROM compras"
        listaCompras = buscarDocumento(query)
    else: listaCompras = buscarDocumento(query, [dadoProcurado])
    
    if not listaCompras:
        print("Nenhuma compra encontrada!")
        return False
    for compra in listaCompras:
        print("===========================================")
        if tipoDado in ["nome_cliente", "id_cliente"]:
            cliente = None
            vendedor = buscarPorId("vendedores", compra.id_vendedor)
        else:
            cliente = buscarPorId("usuarios", compra.id_cliente)
            vendedor = None
        enderecoCliente = buscarPorId("enderecos", compra.endereco_cliente)
        enderecoVendedor = buscarPorId("enderecos", compra.endereco_vendedor)
        produtosCompra = [buscarPorId("produtos", produto_id) for produto_id in compra.produtos]
        formatacaoCompras(compra, cliente, enderecoCliente, vendedor, enderecoVendedor, produtosCompra, comCodigo)
    print("===========================================")
    return listaCompras if len(listaCompras) > 1 else listaCompras[0]