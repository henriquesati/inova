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

## 📚 Relações entre Entidades do Domínio

- `entidade`  
<span style="color:gray"><strong>Entidade (1) ──── (N) Contrato</strong></span><br>
<span style="color:gray"><strong>Entidade (1) ──── (N) Empenho</strong></span>

---

- `fornecedor`  
<span style="color:gray"><strong>Fornecedor (1) ──── (N) Contrato</strong></span><br>
<span style="color:gray"><strong>Fornecedor (1) ──── (N) Empenho</strong></span><br>
<span style="color:gray"><strong>Fornecedor (1) ──── (N) NFe</strong></span>

---

- `contrato`  
<span style="color:gray"><strong>Contrato (1) ──── (N) Empenho</strong></span>

---

- `empenho`  
<span style="color:gray"><strong>Empenho (1) ──── (N) LiquidacaoNotaFiscal</strong></span><br>
<span style="color:gray"><strong>Empenho (1) ──── (N) Pagamento</strong></span>

---

- `liquidacao_nota_fiscal`  
<span style="color:gray"><strong>LiquidacaoNotaFiscal (1) ──── (1) NFe</strong></span>

---

- `nfe`  
<span style="color:gray"><strong>NFe (1) ──── (N) NFePagamento</strong></span>

---

- `pagamento`  
<span style="color:gray"><strong>Pagamento (1) ──── (N) NFePagamento</strong></span>

---

- `nfe_pagamento`  
<span style="color:gray"><strong>NFe (N) ──── (N) Pagamento</strong></span>

---

### 🔴 Relações 1-to-1 Críticas (Invariantes de Domínio)

<span style="color:gray"><strong>LiquidacaoNotaFiscal (1) ──── (1) NFe</strong></span>
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