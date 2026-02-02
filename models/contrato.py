from dataclasses import dataclass
from  datetime import date
from decimal import Decimal
from typing import Optional

@dataclass
class Contrato:
    id_contrato: int
    valor: Decimal
    data: date
    objeto: str
    id_entidade: int
    id_fornecedor: int

    @staticmethod
    def from_row(row: dict) -> "Contrato":
        # aqui você coloca contratos/invariantes
        if row["id_contrato"] is None:
            raise ValueError("Contrato inválido: id_contrato é obrigatório")
        
        return Contrato(
            id_contrato=int(row["id_contrato"]),
            valor=row["valor"],
            data=row["data"],
            objeto=row["objeto"],
            id_entidade=row["id_entidade"],
            id_fornecedor=row["id_fornecedor"],
        )
