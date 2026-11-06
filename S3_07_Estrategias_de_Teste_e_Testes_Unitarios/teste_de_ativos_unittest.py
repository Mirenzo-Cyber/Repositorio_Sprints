import unittest
# Importamos as funções e o nosso "banco de dados" (o dicionário) do ficheiro principal
from ativos_crud import cadastrar_ativo, atualizar_ativo, remover_ativo, inventario_ativos


class TestCRUDAtivos(unittest.TestCase):

    def setUp(self):
        """Este método corre automaticamente ANTES de cada teste."""
        inventario_ativos.clear()  # Limpa o inventário para que cada teste comece do zero

    # --- Testes de Cadastro ---
    def test_cadastrar_ativo_valido(self):
        resultado = cadastrar_ativo("RT-01", "Roteador Core", "Rede", "10.0.0.1")
        self.assertTrue(resultado)
        self.assertIn("RT-01", inventario_ativos)  # Verifica se o ativo foi parar ao dicionário

    def test_cadastrar_ativo_invalido_duplicado(self):
        # Cadastramos a primeira vez (sucesso)
        cadastrar_ativo("RT-01", "Roteador Core", "Rede", "10.0.0.1")
        # Tentamos cadastrar com o mesmo ID (deve falhar)
        resultado = cadastrar_ativo("RT-01", "Outro Roteador", "Rede", "10.0.0.2")
        self.assertFalse(resultado)

    # --- Testes de Atualização ---
    def test_atualizar_ativo_existente(self):
        cadastrar_ativo("FW-01", "Firewall", "Segurança", "192.168.1.1")
        resultado = atualizar_ativo("FW-01", novo_status="Manutenção")
        self.assertTrue(resultado)
        self.assertEqual(inventario_ativos["FW-01"]["status"], "Manutenção")

    # --- Testes de Remoção ---
    def test_remover_ativo_existente(self):
        cadastrar_ativo("SRV-01", "Servidor Web", "Servidor", "10.0.0.5")
        resultado = remover_ativo("SRV-01")
        self.assertTrue(resultado)
        self.assertNotIn("SRV-01", inventario_ativos)

    def test_remover_ativo_inexistente(self):
        resultado = remover_ativo("ID_FANTASMA")
        self.assertFalse(resultado)


if __name__ == '__main__':
    unittest.main()