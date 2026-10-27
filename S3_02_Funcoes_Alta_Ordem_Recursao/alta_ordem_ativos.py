from enum import Enum

class TipoAtivo(Enum):
    COMPUTADORES = "Computadores"
    NOTEBOOKS = "Notebooks"
    SERVIDORES = "Servidores"
    SWITCHES = "Switches"

ARQUIVO_ATIVOS = "ativos.txt"

ativos_ti = {
    "AT-001": {
        "nome": "SRV-DB-PROD",
        "responsavel": "Carlos Silva",
        "setor": "Data Center",
        "tipo": TipoAtivo.SERVIDORES.value,
        "vulnerabilidades": ["CVE-2024-1001", "Porta 22 exposta", "TLS 1.0 ativo"]
    },
    "AT-002": {
        "nome": "SW-CORE-01",
        "responsavel": "Fernanda Costa",
        "setor": "Infraestrutura",
        "tipo": TipoAtivo.SWITCHES.value,
        "vulnerabilidades": ["SNMP padrão (public)"]
    },
    "AT-003": {
        "nome": "NB-SEC-04",
        "responsavel": "Marcos Oliveira",
        "setor": "SOC / Segurança",
        "tipo": TipoAtivo.NOTEBOOKS.value,
        "vulnerabilidades": []
    },
    "AT-004": {
        "nome": "PC-FIN-12",
        "responsavel": "Ana Souza",
        "setor": "Financeiro",
        "tipo": TipoAtivo.COMPUTADORES.value,
        "vulnerabilidades": ["SMB v1 habilitado", "Antivírus desatualizado"]
    },
    "AT-005": {
        "nome": "SRV-WEB-APP",
        "responsavel": "Carlos Silva",
        "setor": "Data Center",
        "tipo": TipoAtivo.SERVIDORES.value,
        "vulnerabilidades": ["Headers HTTP inseguros"]
    }
}

# ==========================================
# 4. Utilizar map() para transformar a lista de ativos
# Exemplo: Transformar os itens do dicionário adicionando a contagem de
# vulnerabilidades e definindo o status de risco de cada equipamento.
# ==========================================
ativos_transformados = list(map(
    lambda item: {
        "id": item[0],
        **item[1],
        "qtd_vulnerabilidades": len(item[1]["vulnerabilidades"]),
        "status_risco": "CRÍTICO" if len(item[1]["vulnerabilidades"]) >= 2
                        else ("ATENÇÃO" if len(item[1]["vulnerabilidades"]) == 1 else "SEGURO")
    },
    ativos_ti.items()
))

# ==========================================
# 5. Utilizar filter() para selecionar ativos por categoria
# Exemplo: Selecionar apenas os ativos da categoria 'Servidores'
# ==========================================
apenas_servidores = dict(filter(
    lambda item: item[1]["tipo"] == TipoAtivo.SERVIDORES.value,
    ativos_ti.items()
))

# ==========================================
# 6. Utilizar lambda em operações de ordenação
# Exemplo: Ordenar os ativos pela quantidade de vulnerabilidades (do mais
# vulnerável para o mais seguro) e, em caso de empate, pelo nome.
# ==========================================
ativos_ordenados_por_risco = sorted(
    ativos_ti.items(),
    key=lambda item: (-len(item[1]["vulnerabilidades"]), item[1]["nome"])
)

# ==========================================
# Exibição dos Resultados
# ==========================================
if __name__ == "__main__":
    print("--- 4. ATIVOS TRANSFORMADOS COM MAP() ---")
    for ativo in ativos_transformados:
        print(f"[{ativo['id']}] {ativo['nome']} ({ativo['setor']}) -> "
              f"Vulns: {ativo['qtd_vulnerabilidades']} | Status: {ativo['status_risco']}")

    print("\n--- 5. FILTRO POR CATEGORIA 'SERVIDORES' COM FILTER() ---")
    for id_ativo, dados in apenas_servidores.items():
        print(f"[{id_ativo}] {dados['nome']} - Resp: {dados['responsavel']}")

    print("\n--- 6. ORDENAÇÃO POR QUANTIDADE DE VULNERABILIDADES (LAMBDA) ---")
    for id_ativo, dados in ativos_ordenados_por_risco:
        qtd = len(dados["vulnerabilidades"])
        print(f"[{id_ativo}] {dados['nome']} ({dados['tipo']}) -> {qtd} vulnerabilidade(s): {dados['vulnerabilidades']}")