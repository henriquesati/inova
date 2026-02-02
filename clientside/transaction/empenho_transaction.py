
import sys
import os
from dataclasses import dataclass, field

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from models.entidade import Entidade
from models.fornecedor import Fornecedor
from models.contrato import Contrato

from typing import Optional
from result import Result

@dataclass
class ContratoEmpenhado:
    entidade: Optional[Entidade]
    fornecedor: Optional[Fornecedor]
    contrato: Contrato


    @staticmethod
    def build_from_contract(contract_result: Result[Contrato]) -> Result["ContratoEmpenhado"]:
        """
        Constrói um ContratoEmpenhado a partir de um Result[Contrato].
        Utiliza os campos id_entidade e id_fornecedor do contrato para buscar
        os objetos completos no banco de dados.
        """
        return contract_result.bind(
            lambda contract: ContratoEmpenhado.build(
                Entidade.get_by_id(contract.id_entidade),
                Fornecedor.get_by_id(contract.id_fornecedor),
                Result.ok(contract)
            )
        )
        
    @staticmethod
    def build(entidade_result: Result[Entidade], fornecedor_result: Result[Fornecedor], contract_result: Result[Contrato]) -> Result["ContratoEmpenhado"]:
        """
        Constrói um ContratoEmpenhado combinando (binding) os Results de Entidade e Fornecedor.
        Se qualquer um for erro, retorna o erro.
        """
        return entidade_result.bind(
            lambda ent: fornecedor_result.bind(
                lambda forn: contract_result.bind(
                    lambda contract: Result.ok(ContratoEmpenhado(entidade=ent, fornecedor=forn, contrato=contract))
                )
            )
        )

    def __post_init__(self):
        # Exemplo de lógica adicional se necessário
        pass
