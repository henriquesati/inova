from dataclasses import dataclass

@dataclass
class Entidade:
    id_entidade: int
    nome: str
    estado: str
    municipio: str
    cnpj: str
