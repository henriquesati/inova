from dataclasses import dataclass
from  datetime import date
from decimal import Decimal
from typing import Optional
from result import Result

@dataclass
class Contrato:
    id_contrato: int
    valor: Decimal
    data: date
    objeto: str
    id_entidade: int
    id_fornecedor: int

    
    def _validate_id(self) -> Result["Contrato"]:
        if not self.id_contrato:
            return Result.err("Contrato inválido: id_contrato é obrigatório")
        return Result.ok(self)

    def _validate_fks(self) -> Result["Contrato"]:
        if not isinstance(self.id_entidade, int):
             return Result.err(f"Contrato inválido: id_entidade deve ser inteiro (recebido: {type(self.id_entidade)})")
        if not isinstance(self.id_fornecedor, int):
             return Result.err(f"Contrato inválido: id_fornecedor deve ser inteiro (recebido: {type(self.id_fornecedor)})")
        return Result.ok(self)

    def _validate_objeto(self) -> Result["Contrato"]:
        if self.objeto and len(self.objeto) > 255:
            return Result.err(f"Contrato inválido: objeto excede 255 caracteres (recebido: {len(self.objeto)})")
        return Result.ok(self)

    def _validate_valor(self) -> Result["Contrato"]:
        if self.valor is None:
            return Result.err("Contrato inválido: valor é obrigatório")
        
        # Tentativa de conversão segura
        if not isinstance(self.valor, Decimal):
            try:
                self.valor = Decimal(self.valor)
            except (InvalidOperation, TypeError):
                 return Result.err(f"Contrato inválido: valor '{self.valor}' não é um Decimal válido")

        # Numeric(15,2) -> Máximo: 9.999.999.999.999,99
        MAX_VALOR = Decimal("9999999999999.99")
        
        if self.valor > MAX_VALOR:
             return Result.err(f"Contrato inválido: valor excede limite de Numeric(15,2) ({MAX_VALOR})")
        
        return Result.ok(self)

    @staticmethod
    def create(row: dict) -> Result["Contrato"]:
        """
        Factory que substitui o construtor direto e o from_row antigo.
        Retorna um Result que contém o Contrato validado ou uma string de erro.
        """
        try:
            contrato = Contrato(
                id_contrato=int(row["id_contrato"]) if row.get("id_contrato") else None, # type: ignore
                valor=row.get("valor"), # type: ignore (será convertido no validate_valor)
                data=row.get("data"),   # type: ignore
                objeto=row.get("objeto"), # type: ignore
                id_entidade=row.get("id_entidade"), # type: ignore
                id_fornecedor=row.get("id_fornecedor") # type: ignore
            )
        except Exception as e:
            return Result.err(f"Erro estrutural ao criar objeto: {str(e)}")

        # Pipeline de Validação (Railway Oriented Programming)
        # O Result.ok inicia o trilho de sucesso.
        # Cada .bind executa a próxima validação APENAS se a anterior foi sucesso.
        return (
            Result.ok(contrato)
            .bind(lambda c: c._validate_id())
            .bind(lambda c: c._validate_fks())
            .bind(lambda c: c._validate_objeto())
            .bind(lambda c: c._validate_valor())
        )