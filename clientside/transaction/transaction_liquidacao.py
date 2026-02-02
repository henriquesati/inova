
import sys
import os
from dataclasses import dataclass

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from models.empenho import Empenho
from models.nfe import Nfe
from models.liquidacao_nota_fiscal import LiquidacaoNotaFiscal

from typing import Optional

@dataclass
class LiquidacaoTransaction:
    empenho: Optional[Empenho]
    nfe: Optional[Nfe]
    liquidacao: Optional[LiquidacaoNotaFiscal]

    def build(result_empenhado: Result[Empenho], result_nfe: Result[Nfe], result_liquidacao: Result[LiquidacaoNotaFiscal]) -> Result["LiquidacaoTransaction"]:
        print()