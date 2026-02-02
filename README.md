# Inova Project

Ferramentas e utilitários para apoiar o desenvolvimento do projeto **Inova**.

Este repositório contém scripts voltados para inspeção rápida do banco e validações auxiliares.

---

## SQL Helper (`sqlhelp.py`)

O `sqlhelp.py` é um utilitário de linha de comando para inspecionar rapidamente a **estrutura (schema)** de tabelas no PostgreSQL.

- nomes das colunas
- tipos
- nullable
- defaults

### Commands

make sql+nome_da_tabela
__Exemplo:__ make sqlnfe

> make sqlnfe <br>
> make sql-contrato

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

📌 Entidade Administrativa

Entidade (1) ──── (N) Contrato<br>
Entidade (1) ──── (N) Empenho

📌 Fornecedor

Fornecedor (1) ──── (N) Contrato<br>
Fornecedor (1) ──── (N) Empenho<br>
Fornecedor (1) ──── (N) NFe

📌 Contrato

Contrato (1) ──── (N) Empenho

📌 Empenho

Empenho (1) ──── (N) LiquidacaoNotaFiscal<br>
Empenho (1) ──── (N) Pagamento<br>

📌 Liquidação / Nota Fiscal

LiquidacaoNotaFiscal (1) ──── (1) NFe<br>

📌 Nota Fiscal Eletrônica (NFe)

NFe (1) ──── (N) NFePagamento<br>

📌 Pagamento

Pagamento (1) ──── (N) NFePagamento<br>

📌 Relação Indireta (via tabela associativa)<br>

NFe (N) ──── (N) Pagamento

🔴 Relações 1-to-1 críticas (invariantes de domínio)<br>

LiquidacaoNotaFiscal (1) ──── (1) NFe
---

## 📊 Views (ETL Output)

Scripts de feeback visual dos outputs relacionados as pipeline ETL em cada etapa do ciclo de vida da transação.

- **Empenho** => `make view-empenhos`

- **Liquidação** => `make view-liquidacao`

- **Pagamento** => `make view-pagamento`


```bash

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
### Domain validation rules e invariantes
As validações sãp centralizadas em contextos transacionais imutáveis, permitindo que cada etapa do ciclo da despesa pública tenha invariantes explícitas e auditáveis centralizadas 
e em referencia ao estagio de vida da transação/objeto. Isso facilita a detecção de anomalias, validações faltantes, e a rastreabilidade do erro e a evolução do domínio sem acoplamento excessivo entre entidades.
Além disso a abordagem é extremamente orientada Ao paradigma declarativo funcional, tornando o código e sua intenção mais legivle e facil de manter.

-TransactionLiquidacao

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