# ativos_crud.py

# O nosso "banco de dados" em memória
inventario_ativos = {}


def cadastrar_ativo(id_ativo, nome, tipo, ip):
    """
    Regista um novo ativo no sistema.
    """
    # Verifica se o ativo já existe (útil para os testes de "cadastro inválido")
    if id_ativo in inventario_ativos:
        print(f"Erro: O ativo com ID '{id_ativo}' já existe.")
        return False

    # Verifica se os dados obrigatórios foram preenchidos
    if not id_ativo or not nome:
        print("Erro: O ID e o Nome são obrigatórios.")
        return False

    # Adiciona o ativo ao dicionário
    inventario_ativos[id_ativo] = {
        'nome': nome,
        'tipo': tipo,
        'ip': ip,
        'status': 'Online'  # Status padrão
    }

    print(f"Sucesso: Ativo '{nome}' cadastrado!")
    return True


# --- Pequeno teste manual ---
if __name__ == "__main__":
    cadastrar_ativo("FW-01", "Firewall Principal", "Segurança", "192.168.1.1")
    print(inventario_ativos)


def atualizar_ativo(id_ativo, novo_nome=None, novo_tipo=None, novo_ip=None, novo_status=None):
    """
    Atualiza os detalhes de um ativo que já existe no sistema.
    """
    # Verifica se o ativo não existe (importante para os testes de atualização inválida)
    if id_ativo not in inventario_ativos:
        print(f"Erro: O ativo com ID '{id_ativo}' não foi encontrado.")
        return False

    # Atualiza apenas os campos que foram fornecidos
    ativo = inventario_ativos[id_ativo]
    if novo_nome:
        ativo['nome'] = novo_nome
    if novo_tipo:
        ativo['tipo'] = novo_tipo
    if novo_ip:
        ativo['ip'] = novo_ip
    if novo_status:
        ativo['status'] = novo_status

    print(f"Sucesso: Ativo '{id_ativo}' atualizado!")
    return True


def remover_ativo(id_ativo):
    """
    Remove um ativo do inventário.
    """
    # Verifica se o ativo não existe antes de tentar apagar
    if id_ativo not in inventario_ativos:
        print(f"Erro: Não é possível remover. O ativo '{id_ativo}' não existe.")
        return False

    # Apaga o registo do dicionário
    del inventario_ativos[id_ativo]
    print(f"Sucesso: Ativo '{id_ativo}' removido do sistema!")
    return True


# --- Teste manual das novas funções ---
if __name__ == "__main__":
    # Testar as funções que acabámos de criar
    cadastrar_ativo("SRV-01", "Servidor Web", "Servidor", "10.0.0.5")

    print("\nInventário antes da atualização:", inventario_ativos)

    atualizar_ativo("SRV-01", novo_status="Offline")
    remover_ativo("FW-01")  # Tentar remover o do exemplo anterior

    print("\nInventário final:", inventario_ativos)