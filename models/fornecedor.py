from dataclasses import dataclass

from result import Result

@dataclass
class Fornecedor:
    id_fornecedor: int
    nome: str
    documento: str

    def validate(self) -> Result["Fornecedor"]:
        """Executa validações do modelo Fornecedor e retorna Result."""
        return (
            Result.ok(self)
            .bind(lambda _: self._validate_id())
            .bind(lambda _: self._validate_nome())
            .bind(lambda _: self._validate_documento())
        )

    def _validate_id(self) -> Result["Fornecedor"]:
        if not self.id_fornecedor:
            return Result.err("Fornecedor inválido: id_fornecedor é obrigatório")
        return Result.ok(self)

    def _validate_nome(self) -> Result["Fornecedor"]:
        if self.nome and len(self.nome) > 255:
             return Result.err(f"Fornecedor inválido: nome excede 255 caracteres (recebido: {len(self.nome)})")
        return Result.ok(self)

    def _validate_documento(self) -> Result["Fornecedor"]:
        # Varchar(20)
        if self.documento and len(self.documento) > 20:
             return Result.err(f"Fornecedor inválido: documento excede 20 caracteres (recebido: {len(self.documento)})")
        return Result.ok(self)

    @staticmethod
    def from_row(row: dict) -> Result["Fornecedor"]:
        try:
            obj = Fornecedor(
                id_fornecedor=int(row["id_fornecedor"]) if row.get("id_fornecedor") else None,
                nome=row.get("nome"),
                documento=row.get("documento")
            )
            return obj.validate()
        except Exception as e:
            return Result.err(f"Erro ao instanciar Fornecedor: {str(e)}")
