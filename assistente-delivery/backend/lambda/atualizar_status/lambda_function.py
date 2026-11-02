import boto3
from decimal import Decimal
from datetime import datetime, timezone

dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
tabela = dynamodb.Table("Pedidos")


def converter_numeros(dado):
    if isinstance(dado, float):
        return Decimal(str(dado))
    if isinstance(dado, list):
        return [converter_numeros(item) for item in dado]
    if isinstance(dado, dict):
        return {chave: converter_numeros(valor) for chave, valor in dado.items()}
    return dado


def lambda_handler(event, context):
    pedido = event.get("pedido", {})
    pagamento_aprovado = event.get("pagamentoAprovado", False)
    pedido_id = pedido.get("pedidoId") or event.get("pedidoId")

    if not pedido_id:
        return {
            "sucesso": False,
            "mensagem": "Identificador do pedido não informado."
        }

    status = "PAGO" if pagamento_aprovado else "PAGAMENTO_RECUSADO"

    item = {
        "pedidoId": pedido_id,
        "cliente": pedido.get("cliente", "Não informado"),
        "produtos": pedido.get("produtos", []),
        "valorTotal": pedido.get("valorTotal", 0),
        "status": status,
        "statusPagamento": event.get(
            "statusPagamento",
            "APROVADO" if pagamento_aprovado else "RECUSADO"
        ),
        "valorPago": event.get("valorPago", pedido.get("valorTotal", 0)),
        "criadoEm": datetime.now(timezone.utc).isoformat()
    }

    item = converter_numeros(item)

    tabela.update_item(
        Key={"pedidoId": pedido_id},
        UpdateExpression=(
            "SET cliente = :cliente, produtos = :produtos, "
            "valorTotal = :valor, #st = :status, "
            "statusPagamento = :pagamento, valorPago = :valorPago, "
            "criadoEm = :data"
        ),
        ExpressionAttributeNames={"#st": "status"},
        ExpressionAttributeValues={
            ":cliente": item["cliente"],
            ":produtos": item["produtos"],
            ":valor": item["valorTotal"],
            ":status": item["status"],
            ":pagamento": item["statusPagamento"],
            ":valorPago": item["valorPago"],
            ":data": item["criadoEm"]
        }
    )

    return {
        "sucesso": True,
        "pedidoId": pedido_id,
        "status": status,
        "mensagem": "Pedido atualizado com sucesso."
    }
