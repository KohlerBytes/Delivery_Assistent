# Estrutura do DynamoDB

Região: `us-east-2`.

## Tabela `Pedidos`

- Chave de partição: `pedidoId` (String).
- Atributos utilizados: `cliente`, `produtos`, `valorTotal`, `status`, `statusPagamento`, `valorPago`, `criadoEm`.
- Capacidade sugerida para o MVP: sob demanda (PAY_PER_REQUEST).

## Tabela `Produtos`

- Chave de partição: `produtoId` (String).
- Atributos utilizados: `nome`, `preco`, `estoque`, `disponivel`.
- Capacidade sugerida para o MVP: sob demanda (PAY_PER_REQUEST).

## Dados de exemplo

Os arquivos `pedidos_exemplo.json` e `produtos_exemplo.json` contêm exemplos no formato DynamoDB JSON (com tipos `S`, `N`, `BOOL`, `L` e `M`).
