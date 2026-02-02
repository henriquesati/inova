from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class Empenho:
    id_empenho: str
    ano: int
    data_empenho: date
    cpf_cnpj_credor: str
    credor: str
    valor: Decimal
    id_entidade: int
    id_contrato: Optional[int] = None
