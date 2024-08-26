from conexaoCassandra import conectar
from formatacao import formatacaoUsuario, formatacaoVendedor, formatacaoProduto, formatacaoCompras
from uuid import UUID
from typing import Union, List, Dict

sessao = conectar()

def buscarDocumento(query: str, parametros: Union[None, List] = None) -> Union[None, List[Dict]]:
    documentos = sessao.execute(query, parametros) if parametros else sessao.execute(query)
    documentos = list(documentos)
    return documentos if documentos else None

def buscarPorId(colecao: str, objectId: Union[str, UUID]) -> Union[None, Dict]:
    try: objectId = UUID(objectId) if not isinstance(objectId, UUID) else objectId
    except ValueError:
        print(f"ID inválido: {objectId}")
        return None
    query = f"SELECT * FROM {colecao} WHERE id = %s"
    dado = list(sessao.execute(query, [objectId]))
    return dado[0] if dado else None

def buscarUsuario(dadoProcurado: Union[str, UUID], tipoDado: str = None, comCodigo: bool = False) -> Union[None, List[Dict], Dict]:
    if tipoDado == 'nome':
        query = "SELECT * FROM usuarios WHERE nome_usuario = %s ALLOW FILTERING" if dadoProcurado else "SELECT * FROM usuarios"
        listaUsuarios = buscarDocumento(query, [dadoProcurado] if dadoProcurado else None)
        if not listaUsuarios:
            print("Nenhum usuário encontrado!")
            return False
        for usuario in listaUsuarios:
            print("===========================================")
            enderecos = [buscarPorId("enderecos", endereco) for endereco in usuario.enderecos or []]
            favoritos = []
            for favorito in usuario.favoritos or []:
                produtoEscolhido = buscarPorId("produtos", favorito)
                vendedorProduto = buscarPorId("vendedores", produtoEscolhido.id_vendedor) if produtoEscolhido else None
                if produtoEscolhido:
                    favoritos.append({
                        "produto": produtoEscolhido,
                        "vendedor": vendedorProduto
                    })
            compras = []
            for compra in usuario.compras or []:
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

def buscarVendedor(dadoProcurado: Union[str, UUID], tipoDado: str = None, comCodigo: bool = False) -> Union[None, List[Dict], Dict]:
    if tipoDado == 'nome':
        query = "SELECT * FROM vendedores WHERE nome_vendedor = %s ALLOW FILTERING" if dadoProcurado else "SELECT * FROM vendedores"
        listaVendedores = buscarDocumento(query, [dadoProcurado] if dadoProcurado else None)
        if not listaVendedores:
            print("Nenhum vendedor encontrado!")
            return False
        for vendedor in listaVendedores:
            print("===========================================")
            enderecos = [buscarPorId("enderecos", endereco) for endereco in vendedor.enderecos or []]
            produtos = [buscarPorId("produtos", produto_id) for produto_id in vendedor.produtos or []]
            vendas = []
            for venda in vendedor.vendas or []:
                vendaFeita = buscarPorId("vendas", venda)
                if vendaFeita:
                    cliente = buscarPorId("usuarios", vendaFeita.id_cliente)
                    enderecoCliente = buscarPorId("enderecos", vendaFeita.endereco_cliente)
                    produtosVenda = [buscarPorId("produtos", produto_id) for produto_id in vendaFeita.produtos]
                    vendas.append({
                        'venda': vendaFeita,
                        'cliente': cliente,
                        'enderecoCliente': enderecoCliente,
                        'produtos': produtosVenda
                    })
            formatacaoVendedor(vendedor, enderecos, produtos, vendas, comCodigo)
        print("===========================================")
        return listaVendedores if len(listaVendedores) > 1 else (listaVendedores[0] if listaVendedores else None)
    return buscarPorId("vendedores", dadoProcurado)

def buscarProduto(dadoProcurado: Union[str, UUID], tipoDado: str = None, comCodigo: bool = False, comVendedor: bool = False) -> Union[None, List[Dict], Dict]:
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
        return listaProdutos if len(listaProdutos) > 1 else (listaProdutos[0] if listaProdutos else None)
    return buscarPorId("produtos", dadoProcurado)

def buscarCompra(dadoProcurado: Union[str, UUID], tipoDado: str = None, comCodigo: bool = False) -> Union[None, List[Dict], Dict]:
    if tipoDado == 'nome_cliente': query = "SELECT * FROM compras WHERE nome_cliente = %s ALLOW FILTERING"
    elif tipoDado == 'id_cliente': query = "SELECT * FROM compras WHERE id_cliente = %s ALLOW FILTERING"
    elif tipoDado == 'nome_vendedor': query = "SELECT * FROM compras WHERE nome_vendedor = %s ALLOW FILTERING"
    elif tipoDado == 'id_vendedor': query = "SELECT * FROM compras WHERE id_vendedor = %s ALLOW FILTERING"
    else: return buscarPorId("compras", dadoProcurado)

    listaCompras = buscarDocumento(query, [dadoProcurado] if dadoProcurado else None)
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
    return listaCompras if len(listaCompras) > 1 else (listaCompras[0] if listaCompras else None)