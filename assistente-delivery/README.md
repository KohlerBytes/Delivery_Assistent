# Assistente de Delivery — AWS Serverless

Projeto acadêmico de um assistente de delivery usando AWS Lambda, Amazon DynamoDB e AWS Step Functions.

## Arquitetura

- **AWS Lambda / Python 3.12**: valida pedido, consulta estoque, simula pagamento e atualiza o pedido.
- **Amazon DynamoDB**: armazena pedidos e catálogo de produtos.
- **AWS Step Functions Standard**: orquestra o fluxo de processamento.
- **Região prevista**: `us-east-2` (US East – Ohio).

> Este repositório contém os códigos-fonte e arquivos de configuração para implantação. Ele não contém credenciais, ARNs reais ou recursos provisionados na conta AWS.

## Estrutura

```text
assistente-delivery/
├── backend/
│   ├── lambda/
│   │   ├── validar_pedido/lambda_function.py
│   │   ├── verificar_estoque/lambda_function.py
│   │   ├── processar_pagamento/lambda_function.py
│   │   └── atualizar_status/lambda_function.py
│   └── state_machine/
│       ├── delivery_workflow.json
│       └── iam_policy_step_functions.json
├── database/
│   ├── estrutura_dynamodb.md
│   ├── pedidos_exemplo.json
│   └── produtos_exemplo.json
├── documentation/
│   ├── arquitetura.md
│   ├── requisitos.md
│   ├── manual_execucao.md
│   └── testes.md
├── .gitignore
└── README.md
```

## Recursos AWS necessários

1. Tabela DynamoDB `Pedidos`, chave de partição `pedidoId` (String).
2. Tabela DynamoDB `Produtos`, chave de partição `produtoId` (String).
3. Quatro funções Lambda com os nomes indicados na documentação.
4. Uma máquina AWS Step Functions Standard chamada `AssistenteDeliveryWorkflow`.
5. Uma role IAM para a máquina de estados invocar as quatro funções.

## Configuração antes da implantação

1. Crie os recursos na região `us-east-2`.
2. Publique cada arquivo `lambda_function.py` na função Lambda correspondente.
3. Configure a role de execução das Lambdas conforme `documentation/manual_execucao.md`.
4. Abra `backend/state_machine/delivery_workflow.json`.
5. Substitua os quatro marcadores `SUBSTITUIR_PELO_ARN_...` pelos ARNs reais das Lambdas.
6. Crie a máquina de estados usando o JSON ASL.
7. Configure a role da Step Functions com a política de `backend/state_machine/iam_policy_step_functions.json`, substituindo os marcadores pelos ARNs reais.

## Evento de teste

Use o arquivo `documentation/testes.md` para os eventos de aprovação, recusa, produto inexistente e estoque insuficiente.

## Limitações atuais do MVP

- Pagamento é simulado; não existe integração com banco ou gateway.
- A função de estoque consulta disponibilidade, mas **não reserva nem desconta** unidades.
- O fluxo ainda não possui interface web/API Gateway nem integração com Amazon Bedrock.
- O fluxo não implementa compensação automática nem idempotência para pedidos repetidos.
- O projeto é uma base acadêmica/MVP; não deve ser usado em produção sem controles adicionais de segurança, concorrência, observabilidade e tratamento de falhas.

## Custos e segurança

Os serviços AWS podem gerar cobranças, mesmo em projetos pequenos. Monitore o consumo e os créditos disponíveis. Nunca versione credenciais, chaves de acesso, tokens, dados pessoais reais ou arquivos `.env`.
