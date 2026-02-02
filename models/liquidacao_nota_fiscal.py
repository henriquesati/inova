from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class LiquidacaoNotaFiscal:
    id_liq_empnf: int
    chave_danfe: str
    data_emissao: date
    valor: Decimal
    id_empenho: str
