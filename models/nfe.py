from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Nfe:
    id: int
    chave_nfe: str
    numero_nfe: str
    data_hora_emissao: datetime
    cnpj_emitente: str
    valor_total_nfe: Decimal
