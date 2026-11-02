import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
tabela = dynamodb.Table("Produtos")


def lambda_handler(event, context):
    if not event.get("valido"):
        return {
            "estoqueDisponivel": False,
            "mensagem": "O pedido não foi validado.",
            "erros": ["Pedido inválido."]
        }

    pedido = event.get("pedido", {})
    produtos = pedido.get("produtos", [])

    resultados = []
    erros = []
    estoque_suficiente = True

    for produto in produtos:
        produto_id = produto.get("produtoId")
        quantidade = produto.get("quantidade")

        if not produto_id or quantidade is None:
            erros.append("Produto sem produtoId ou quantidade.")
            estoque_suficiente = False
            continue

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            erros.append(f"Quantidade inválida para o produto {produto_id}.")
            estoque_suficiente = False
            continue

        resposta = tabela.get_item(Key={"produtoId": produto_id})
        item = resposta.get("Item")

        if not item:
            erros.append(f"Produto {produto_id} não encontrado.")
            estoque_suficiente = False
            continue

        estoque_atual = int(item.get("estoque", 0))
        disponivel = item.get("disponivel", False)
        suficiente = bool(disponivel) and estoque_atual >= quantidade

        if not suficiente:
            estoque_suficiente = False
            erros.append(f"Estoque insuficiente para {item.get('nome', produto_id)}.")

        resultados.append({
            "produtoId": produto_id,
            "nome": item.get("nome"),
            "quantidadeSolicitada": quantidade,
            "estoqueAtual": estoque_atual,
            "estoqueSuficiente": suficiente
        })

    return {
        "estoqueDisponivel": estoque_suficiente,
        "pedido": pedido,
        "produtosVerificados": resultados,
        "erros": erros
    }
