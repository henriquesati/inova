
import sys
import os
from dataclasses import dataclass, field

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from models.entidade import Entidade
from models.fornecedor import Fornecedor

from typing import Optional
from result import Result

@dataclass
class ContratoEmpenhado:
    entidade: Optional[Entidade]
    fornecedor: Optional[Fornecedor]


    def build_from_contract(contract: Result[Contract])
    @staticmethod
    def build(entidade_result: Result[Entidade], fornecedor_result: Result[Fornecedor]) -> Result["ContratoEmpenhado"]:
        """
        Constrói um ContratoEmpenhado combinando (binding) os Results de Entidade e Fornecedor.
        Se qualquer um for erro, retorna o erro.
        """
        return entidade_result.bind(
            lambda ent: fornecedor_result.bind(
                lambda forn: Result.ok(ContratoEmpenhado(entidade=ent, fornecedor=forn))
            )
        )

    def __post_init__(self):
        # Exemplo de lógica adicional se necessário
        pass

