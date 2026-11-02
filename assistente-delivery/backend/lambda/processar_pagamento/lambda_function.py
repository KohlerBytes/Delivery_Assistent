def lambda_handler(event, context):
    if not event.get("estoqueDisponivel", False):
        return {
            "pagamentoAprovado": False,
            "mensagem": "Pagamento não processado: estoque indisponível."
        }

    pedido = event.get("pedido", {})
    pedido_id = pedido.get("pedidoId")
    valor_total = pedido.get("valorTotal")

    if not pedido_id or valor_total is None:
        return {
            "pagamentoAprovado": False,
            "mensagem": "Dados do pedido incompletos."
        }

    try:
        valor_total = float(valor_total)
        if valor_total <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        return {
            "pagamentoAprovado": False,
            "mensagem": "Valor do pedido inválido."
        }

    # Simulação acadêmica: não processa pagamentos reais.
    aprovado = event.get("simularAprovacao", True)

    if aprovado:
        return {
            "pagamentoAprovado": True,
            "pedidoId": pedido_id,
            "valorPago": valor_total,
            "statusPagamento": "APROVADO",
            "mensagem": "Pagamento aprovado com sucesso."
        }

    return {
        "pagamentoAprovado": False,
        "pedidoId": pedido_id,
        "valorPago": valor_total,
        "statusPagamento": "RECUSADO",
        "mensagem": "Pagamento recusado."
    }
