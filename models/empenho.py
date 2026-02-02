from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional, List
from result import Result
from db_connection import get_db_connection

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

    @staticmethod
    def from_row(row: dict) -> Result["Empenho"]:
        try:
             # Basic instantiation - validation could be added later similar to other models
            empenho = Empenho(
                id_empenho=row["id_empenho"],
                ano=row["ano"],
                data_empenho=row["data_empenho"],
                cpf_cnpj_credor=row["cpf_cnpj_credor"],
                credor=row["credor"],
                valor=row["valor"],
                id_entidade=row["id_entidade"],
                id_contrato=row.get("id_contrato")
            )
            return Result.ok(empenho)
        except Exception as e:
            return Result.err(f"Erro ao instanciar Empenho: {str(e)}")

    @staticmethod
    def get_by_contract_id(id_contrato: int) -> Result[List["Empenho"]]:
        """Busca empenhos pelo id_contrato."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empenho WHERE id_contrato = %s", (id_contrato,))
            rows = cursor.fetchall()
            
            if not rows:
                 cursor.close()
                 conn.close()
                 # Retornar lista vazia é sucesso, não erro? 
                 # O user pediu "Empenho.domain.get_by_contractid". 
                 # Se não achar, retorna lista vazia wrapped em Result.ok
                 return Result.ok([])

            columns = [desc[0] for desc in cursor.description]
            
            empenhos = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                res = Empenho.from_row(row_dict)
                if res.is_err:
                    cursor.close()
                    conn.close()
                    return Result.err(f"Erro ao converter linha de empenho: {res.error}")
                empenhos.append(res.value)
            
            cursor.close()
            conn.close()
            
            return Result.ok(empenhos)
            
        except Exception as e:
            return Result.err(f"Erro ao buscar Empenhos por contrato: {str(e)}")
