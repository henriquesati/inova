import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from result import Result
from models.entidade import Entidade
from models.fornecedor import Fornecedor
from clientside.transaction.empenho_transaction import ContratoEmpenhado
from clientside.domains.empenho import executar_empenho_rules

class TestEmpenhoFlow(unittest.TestCase):
    
    def setUp(self):
        self.valid_entidade = Entidade(
            id_entidade=1,
            nome="Prefeitura Teste",
            estado="SP",
            municipio="Sao Paulo",
            cnpj="12345678000199"
        )
        self.valid_fornecedor = Fornecedor(
            id_fornecedor=1,
            nome="Fornecedor Teste",
            documento="11122233344"
        )

    def test_success_flow(self):
        """
        Test Case 1: Success Flow
        Valid Entidade and Fornecedor Results should bind correctly into a ContratoEmpenhado,
        and pass all domain rules.
        """
        res_entidade = Result.ok(self.valid_entidade)
        res_fornecedor = Result.ok(self.valid_fornecedor)

        res_contrato = ContratoEmpenhado.build(res_entidade, res_fornecedor)
        self.assertTrue(res_contrato.is_ok, f"Binding failed: {res_contrato._error}")
        
        contrato = res_contrato.value
        self.assertIsInstance(contrato, ContratoEmpenhado)
        self.assertEqual(contrato.entidade, self.valid_entidade)
        self.assertEqual(contrato.fornecedor, self.valid_fornecedor)
        print(f"\n[Visual Log] Contrato (Success): {contrato}")

        res_rules = executar_empenho_rules(contrato)
        self.assertTrue(res_rules.is_ok, f"Rules failed: {res_rules._error}")
        self.assertEqual(res_rules.value, contrato)
        print(f"[Visual Log] Rules Result (Success): {res_rules}")

    def test_success_unwrapped_params(self):
        """
        Test Case 6a: Success Variations - Unwrapped Parameters
        Test behavior when passing objects in their unwrapped form (via constructor).
        """
        # 1. Unwrapped Form (Direct Constructor)
        contrato_unwrapped = ContratoEmpenhado(
            entidade=self.valid_entidade,
            fornecedor=self.valid_fornecedor
        )
        print(f"\n[Visual Log] Success Unwrapped (Constructor): {contrato_unwrapped}")
        
        # Verify it holds the data correctly
        self.assertEqual(contrato_unwrapped.entidade, self.valid_entidade)
        self.assertEqual(contrato_unwrapped.fornecedor, self.valid_fornecedor)

    def test_success_wrapped_params(self):
        """
        Test Case 6b: Success Variations - Wrapped Parameters
        Test behavior when passing objects in their wrapped form (via build factory).
        """
        # 2. Wrapped Form (Build Factory)
        res_entidade = Result.ok(self.valid_entidade)
        res_fornecedor = Result.ok(self.valid_fornecedor)
        
        res_contrato_wrapped = ContratoEmpenhado.build(res_entidade, res_fornecedor)
        print(f"[Visual Log] Success Wrapped (Build Factory): {res_contrato_wrapped}")

        self.assertTrue(res_contrato_wrapped.is_ok)
        contrato_wrapped = res_contrato_wrapped.value
        
        self.assertIsInstance(contrato_wrapped, ContratoEmpenhado)
        self.assertEqual(contrato_wrapped.entidade, self.valid_entidade)
        self.assertEqual(contrato_wrapped.fornecedor, self.valid_fornecedor)

    def test_circuit_breaker_entidade_error(self):
        """
        Test Case 2: Circuit Breaker - Entidade Error
        If Entidade Result is an error, ContratoEmpenhado.build should return that error
        immediately (circuit breaker).
        """
        error_msg = "Entidade not found"
        res_entidade = Result.err(error_msg)
        res_fornecedor = Result.ok(self.valid_fornecedor)

        res_contrato = ContratoEmpenhado.build(res_entidade, res_fornecedor)
        
        self.assertTrue(res_contrato.is_err)
        self.assertEqual(res_contrato.error, error_msg)
        
        print(f"\n[Visual Log] Result Entidade Error: {res_contrato}")

    def test_circuit_breaker_fornecedor_error(self):
        """
        Test Case 3: Circuit Breaker - Fornecedor Error
        If Fornecedor Result is an error, ContratoEmpenhado.build should return that error
        immediately (circuit breaker).
        """
        error_msg = "Fornecedor not found"
        res_entidade = Result.ok(self.valid_entidade)
        res_fornecedor = Result.err(error_msg)

        res_contrato = ContratoEmpenhado.build(res_entidade, res_fornecedor)
        
        self.assertTrue(res_contrato.is_err)
        self.assertEqual(res_contrato.error, error_msg)

        print(f"\n[Visual Log] Result Fornecedor Error: {res_contrato}")

    def test_invariants_entidade_invalid(self):
        """
        Test Case 4: Transformation into Error - Domain Invariants (Entidade)
        Parameterized test with a list of invalid entities.
        """
        invalid_entidades = [
            # Case: id_entidade missing
            Entidade(id_entidade=0, nome="Valid", estado="SP", municipio="SP", cnpj="123"),
            # Case: nome too long (>255)
            Entidade(id_entidade=1, nome="a" * 256, estado="SP", municipio="SP", cnpj="123"),
            # Case: estado too long (>50)
            Entidade(id_entidade=1, nome="Valid", estado="a" * 51, municipio="SP", cnpj="123"),
            # Case: municipio too long (>100)
            Entidade(id_entidade=1, nome="Valid", estado="SP", municipio="a" * 101, cnpj="123"),
            # Case: cnpj too long (>20)
            Entidade(id_entidade=1, nome="Valid", estado="SP", municipio="SP", cnpj="a" * 21),
            # Case: Entidade is None (handled by domain rule check)
            None 
        ]

        for i, invalid_entidade in enumerate(invalid_entidades):
            with self.subTest(i=i, entidade=invalid_entidade):
                # If we pass None in Result, it's ok for build, but fails rules
                res_entidade = Result.ok(invalid_entidade)
                res_fornecedor = Result.ok(self.valid_fornecedor)

                res_contrato = ContratoEmpenhado.build(res_entidade, res_fornecedor)
                self.assertTrue(res_contrato.is_ok)
                
                contrato = res_contrato.value
                
                # Execute rules - should fail due to invalid entity
                res_rules = executar_empenho_rules(contrato)
                
                self.assertTrue(res_rules.is_err, f"Should fail for invalid entidade: {invalid_entidade}")
                print(f"[Visual Log] Invariant Test (Entidade invalid): {res_rules}")

    def test_invariants_fornecedor_invalid(self):
        """
        Test Case 5: Transformation into Error - Domain Invariants (Fornecedor)
        Parameterized test with a list of invalid fornecedores.
        """
        invalid_fornecedores = [
            # Case: id_fornecedor missing
            Fornecedor(id_fornecedor=0, nome="Valid", documento="123"),
            # Case: nome too long (>255)
            Fornecedor(id_fornecedor=1, nome="a" * 256, documento="123"),
            # Case: documento too long (>20)
            Fornecedor(id_fornecedor=1, nome="Valid", documento="a" * 21),
            # Case: Fornecedor is None
            None
        ]

        for i, invalid_fornecedor in enumerate(invalid_fornecedores):
            with self.subTest(i=i, fornecedor=invalid_fornecedor):
                res_entidade = Result.ok(self.valid_entidade)
                res_fornecedor = Result.ok(invalid_fornecedor)

                res_contrato = ContratoEmpenhado.build(res_entidade, res_fornecedor)
                self.assertTrue(res_contrato.is_ok)
                
                contrato = res_contrato.value

                res_rules = executar_empenho_rules(contrato)
                
                self.assertTrue(res_rules.is_err, f"Should fail for invalid fornecedor: {invalid_fornecedor}")
                print(f"[Visual Log] Invariant Test (Fornecedor invalid): {res_rules}")

if __name__ == "__main__":
    unittest.main()
