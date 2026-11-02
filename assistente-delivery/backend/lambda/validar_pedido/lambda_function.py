from decimal import Decimal, InvalidOperation


def lambda_handler(event, context):
    erros = []

    pedido_id = event.get("pedidoId")
    cliente = event.get("cliente")
    produtos = event.get("produtos", [])

    if not pedido_id:
        erros.append("O identificador do pedido é obrigatório.")

    if not cliente:
        erros.append("O nome do cliente é obrigatório.")

    if not isinstance(produtos, list) or not produtos:
        erros.append("O pedido precisa conter pelo menos um produto.")

    valor_total = Decimal("0.00")

    if isinstance(produtos, list):
        for indice, produto in enumerate(produtos):
            if not isinstance(produto, dict):
                erros.append(f"Produto na posição {indice} possui formato inválido.")
                continue

            produto_id = produto.get("produtoId")
            nome = produto.get("nome")
            quantidade = produto.get("quantidade")
            preco = produto.get("preco")

            if not produto_id:
                erros.append(f"Produto na posição {indice} não possui produtoId.")

            if not nome:
                erros.append(f"Produto na posição {indice} não possui nome.")

            try:
                quantidade = int(quantidade)
                preco = Decimal(str(preco))

                if quantidade <= 0:
                    erros.append(f"Quantidade inválida para {nome or produto_id}.")

                if not preco.is_finite() or preco < 0:
                    erros.append(f"Preço inválido para {nome or produto_id}.")

                if quantidade > 0 and preco.is_finite() and preco >= 0:
                    valor_total += preco * quantidade

            except (ValueError, TypeError, InvalidOperation):
                erros.append(
                    f"Quantidade ou preço inválido para {nome or produto_id}."
                )

    if erros:
        return {"valido": False, "erros": erros}

    pedido = {
        "pedidoId": pedido_id,
        "cliente": cliente,
        "produtos": produtos,
        "valorTotal": float(valor_total),
        "status": "VALIDADO"
    }

    return {"valido": True, "pedido": pedido}
