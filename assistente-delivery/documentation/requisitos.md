# Requisitos do projeto

## Objetivo

Desenvolver um protótipo de assistente de delivery utilizando serviços AWS serverless para validar pedidos, verificar estoque, simular pagamentos e registrar status.

## Requisitos funcionais

- RF01: receber dados de um pedido.
- RF02: validar identificador, cliente e produtos.
- RF03: validar `produtoId`, quantidade e preço.
- RF04: calcular o valor total.
- RF05: consultar produtos e estoque no DynamoDB.
- RF06: rejeitar pedidos com produto inexistente ou estoque insuficiente.
- RF07: simular aprovação ou recusa de pagamento.
- RF08: registrar pedidos pagos ou recusados no DynamoDB.
- RF09: orquestrar as etapas por AWS Step Functions.

## Requisitos não funcionais

- RNF01: utilizar Python 3.12 nas funções Lambda.
- RNF02: utilizar a região AWS `us-east-2`.
- RNF03: aplicar permissões IAM de menor privilégio.
- RNF04: registrar execuções e erros no CloudWatch Logs.
- RNF05: não armazenar credenciais ou dados financeiros reais no repositório.
- RNF06: manter custos reduzidos para uso acadêmico.

## Fora do escopo atual

- Processamento financeiro real.
- Aplicativo móvel completo.
- Integração com Amazon Bedrock.
- Reserva e baixa transacional de estoque.
- API pública e autenticação de clientes.
