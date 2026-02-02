# Inova Project

Ferramentas e utilitários para apoiar o desenvolvimento do projeto **Inova**.

Este repositório contém scripts voltados para inspeção rápida do banco e validações auxiliares.

---

## SQL Helper (`sqlhelp.py`)

O `sqlhelp.py` é um utilitário de linha de comando para inspecionar rapidamente a **estrutura (schema)** de tabelas no PostgreSQL.

### Objetivo

O objetivo do SQL Helper é fornecer um **feedback visual rápido** das entidades do banco — isto é, uma forma simples de consultar:

- nomes das colunas
- tipos
- nullable
- defaults

Sem precisar abrir IDE, DBeaver, pgAdmin ou escrever queries manualmente.

> O script não cria nem altera tabelas: ele apenas consulta metadados.

---

## Entidades do banco (tabelas)

O banco modela os estágios da despesa pública: **Contratação → Empenho → Liquidação → Pagamento**, além de cadastros auxiliares.

As tabelas presentes no banco (conforme dicionário de dados) são:

- `contrato`
- `empenho`
- `liquidacao_nota_fiscal`
- `nfe`
- `pagamento`
- `nfe_pagamento`
- `fornecedor`
- `entidade`

---

## Como usar

### 1) Consulta direta por nome de tabela

```bash
python3 sqlhelp.py <nome_tabela>


### Escopos de teste
**Exemplos de perguntas para investigar** **(você pode e deve criar outras)**:

- Há pagamentos sem empenhos correspondentes?
- Existem contratos com pagamentos acima do valor total contratado?
--------- indagações-------
- essa entidade que tem relação one-to-one ta tendo a propriedade quebrada? Ex: mesma nf compartilhada como comprovante por multiplos contratos
- data de criação da nf bate com a data de pagamento? Ex: criada antes do inicio do contrato
-