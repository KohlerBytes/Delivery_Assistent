# Manual de execução e implantação

## Pré-requisitos

- Conta AWS com acesso aos serviços Lambda, DynamoDB, Step Functions e IAM.
- Região `us-east-2`.
- Tabelas `Pedidos` e `Produtos`.
- Python 3.12 para testes locais, se desejado.

## 1. Criar tabelas DynamoDB

### `Pedidos`

- Partition key: `pedidoId` (String).

### `Produtos`

- Partition key: `produtoId` (String).

Cadastrar os produtos de exemplo usando `database/produtos_exemplo.json`. O console DynamoDB permite inserir cada item individualmente; o arquivo contém uma lista de itens e não deve ser colado inteiro como se fosse um único item.

## 2. Criar as quatro funções Lambda

Criar funções Python 3.12 com estes nomes:

- `validar_pedido`
- `verificar_estoque`
- `processar_pagamento`
- `atualizar_status`

Em cada função, publicar o arquivo `lambda_function.py` correspondente.

## 3. Permissões das Lambdas

A role de `verificar_estoque` precisa permitir `dynamodb:GetItem` na tabela `Produtos`.

Exemplo de política (substitua o ARN da tabela se necessário):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["dynamodb:GetItem"],
    "Resource": "arn:aws:dynamodb:us-east-2:SEU_ACCOUNT_ID:table/Produtos"
  }]
}
```

A role de `atualizar_status` precisa permitir `dynamodb:UpdateItem` na tabela `Pedidos`:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["dynamodb:UpdateItem"],
    "Resource": "arn:aws:dynamodb:us-east-2:SEU_ACCOUNT_ID:table/Pedidos"
  }]
}
```

As funções `validar_pedido` e `processar_pagamento` não precisam de permissões DynamoDB.

## 4. Configurar Step Functions

1. Criar uma máquina de estado do tipo Standard.
2. Usar o conteúdo de `backend/state_machine/delivery_workflow.json`.
3. Substituir os quatro marcadores `SUBSTITUIR_PELO_ARN_...` pelos ARNs reais.
4. Criar ou selecionar uma role de execução com permissão `lambda:InvokeFunction` apenas para as quatro funções.
5. Usar `backend/state_machine/iam_policy_step_functions.json` como base da política da role.
6. Salvar a máquina como `AssistenteDeliveryWorkflow`.

## 5. Executar

Na máquina de estados, iniciar uma execução e colar um dos eventos documentados em `testes.md`.

## 6. Verificar resultados

- Conferir o resultado da execução no Step Functions.
- Conferir os logs das Lambdas no CloudWatch.
- Conferir os registros na tabela `Pedidos`.

## Atenção

Os ARNs e nomes de recursos devem corresponder aos recursos reais da conta. Não publique IDs de conta, credenciais, access keys ou dados pessoais no GitHub.
