# Plano de testes

Todos os eventos abaixo devem ser iniciados na máquina Step Functions `AssistenteDeliveryWorkflow`.

## Teste 1 — Pedido válido e pagamento aprovado

Esperado: fluxo conclui com `sucesso: true`, status `PAGO`, e pedido gravado na tabela `Pedidos`.

```json
{
  "pedidoId": "PED004",
  "cliente": "Cliente Teste",
  "produtos": [
    {
      "produtoId": "PROD001",
      "nome": "Hamburguer",
      "quantidade": 2,
      "preco": 25.00
    },
    {
      "produtoId": "PROD003",
      "nome": "Refrigerante",
      "quantidade": 1,
      "preco": 8.00
    }
  ],
  "simularAprovacao": true
}
```

Valor esperado: R$ 58,00.

## Teste 2 — Pedido válido e pagamento recusado

Use outro identificador, por exemplo `PED005`, e altere `simularAprovacao` para `false`.

Esperado: status `PAGAMENTO_RECUSADO` na tabela `Pedidos`.

## Teste 3 — Produto inexistente

Use `produtoId` inexistente, por exemplo `PROD999`, mantendo os demais dados válidos.

Esperado: `ESTOQUE_INDISPONIVEL`, com erro indicando que o produto não foi encontrado. O pagamento não deve ser invocado.

## Teste 4 — Estoque insuficiente

Solicite uma quantidade maior que o estoque cadastrado, por exemplo 999 unidades de `PROD001`.

Esperado: `ESTOQUE_INDISPONIVEL`. O pagamento não deve ser invocado.

## Teste 5 — Pedido inválido

Exemplo: omitir o campo `cliente` ou informar uma lista `produtos` vazia.

Esperado: `PEDIDO_INVALIDO`, com os erros de validação.

## Observação sobre testes

Use identificadores novos em cada teste para evitar sobrescrever registros anteriores. A função `atualizar_status` usa `UpdateItem`, que cria o item caso ele ainda não exista.
