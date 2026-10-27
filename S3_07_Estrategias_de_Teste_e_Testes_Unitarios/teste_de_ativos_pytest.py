import pytest
from ativos_crud import cadastrar_ativo, atualizar_ativo, remover_ativo, inventario_ativos

# O Pytest usa "fixtures" em vez do setUp.
# "autouse=True" faz com que esta função corra antes de cada teste automaticamente.
@pytest.fixture(autouse=True)
def limpar_inventario():
    inventario_ativos.clear()

# --- Testes de Cadastro ---
def test_cadastrar_ativo_valido():
    assert cadastrar_ativo("SW-01", "Switch Principal", "Rede", "192.168.0.1") == True
    assert "SW-01" in inventario_ativos

def test_cadastrar_ativo_invalido_duplicado():
    cadastrar_ativo("SW-01", "Switch Principal", "Rede", "192.168.0.1")
    assert cadastrar_ativo("SW-01", "Switch Backup", "Rede", "192.168.0.2") == False

# --- Testes de Atualização ---
def test_atualizar_ativo_existente():
    cadastrar_ativo("SW-01", "Switch Principal", "Rede", "192.168.0.1")
    assert atualizar_ativo("SW-01", novo_status="Offline") == True
    assert inventario_ativos["SW-01"]["status"] == "Offline"

# --- Testes de Remoção ---
def test_remover_ativo_existente():
    cadastrar_ativo("SW-01", "Switch Principal", "Rede", "192.168.0.1")
    assert remover_ativo("SW-01") == True
    assert "SW-01" not in inventario_ativos

def test_remover_ativo_inexistente():
    assert remover_ativo("ID_FANTASMA") == False


# --- Novos Testes para aumentar a Cobertura ---

def test_cadastrar_ativo_dados_incompletos():
    # Tenta cadastrar com ID vazio e depois com Nome vazio
    assert cadastrar_ativo("", "Nome Teste", "Rede", "10.0.0.1") == False
    assert cadastrar_ativo("ID-TESTE", "", "Rede", "10.0.0.1") == False


def test_atualizar_ativo_inexistente():
    # Tenta atualizar um ID que não existe no sistema
    assert atualizar_ativo("ID_FANTASMA", novo_status="Offline") == False


def test_atualizar_ativo_multiplos_campos():
    # Cobre os outros 'if' da função de atualização testando a alteração de Nome, Tipo e IP
    cadastrar_ativo("RT-99", "Roteador Antigo", "Rede", "192.168.1.1")
    resultado = atualizar_ativo("RT-99", novo_nome="Roteador Novo", novo_tipo="Infra", novo_ip="10.0.0.1")

    assert resultado == True
    assert inventario_ativos["RT-99"]["nome"] == "Roteador Novo"
    assert inventario_ativos["RT-99"]["tipo"] == "Infra"
    assert inventario_ativos["RT-99"]["ip"] == "10.0.0.1"