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



### 3. Ciclo de Vida do Contrato (Transaction Lifecycle)

Podemos definir o ciclo de vida do contrato — expandindo o significado para além da representação em banco — como uma transação composta por estados sequenciais: **Início, Meio e Fim**.

*   **Início (TransactionEmpenho)**:
    *   Fase inicial da transação.
    *   **Foco**: Reserva de orçamento e formalização do compromisso.
    *   **Requisitos**: Validação de documentos básicos e verificações técnicas preliminares.

*   **Meio (TransactionLiquidação)**:
    *   Fase intermediária, de maior complexidade.
    *   **Foco**: Reconhecimento da dívida após a entrega do bem ou serviço.
    *   **Requisitos**: Consolidação de maior volume de dados (notas fiscais, medições) e alta necessidade de aferição técnica.

*   **Fim (Pagamento)**:
    *   Encerramento financeiro da obrigação.

---

### 4. Escopos de Teste e Validação

Exemplos de perguntas críticas que o sistema de validação deve responder para garantir a integridade dos dados:

**Integridade Financeira**
-   Há pagamentos registrados sem empenhos correspondentes?
-   Existem contratos cuja soma de pagamentos supera o valor total contratado?

**Integridade Relacional e Temporal**
-   **Violação de Propriedade (One-to-One)**: Entidades exclusivas (como uma Nota Fiscal específica) estão sendo compartilhadas incorretamente entre múltiplos contratos?
-   **Coerência Cronológica**:
    -   A data de emissão da Nota Fiscal é compatível com a vigência do contrato?
    -   Existem NFs criadas *antes* da assinatura do contrato ou da nota de empenho?