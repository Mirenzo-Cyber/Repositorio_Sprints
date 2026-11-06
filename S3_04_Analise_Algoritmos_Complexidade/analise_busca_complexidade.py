import time

# ==========================================
# Exercício 1 & 2: Busca Linear vs. Busca Binária
# ==========================================

def busca_linear(lista_ids, alvo):
    """Busca Linear: percorre elemento por elemento. Complexidade: O(n)"""
    for i in range(len(lista_ids)):
        if lista_ids[i] == alvo:
            return i
    return -1


def busca_binaria(lista_ids_ordenada, alvo):
    """Busca Binária: divide o espaço de busca ao meio. Complexidade: O(log n)"""
    inicio = 0
    fim = len(lista_ids_ordenada) - 1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        if lista_ids_ordenada[meio] == alvo:
            return meio
        elif lista_ids_ordenada[meio] < alvo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


# ==========================================
# Teste prático de desempenho e escalabilidade
# ==========================================
if __name__ == "__main__":
    # Simulando uma base grande de 100.000 IDs de ativos de TI
    ativos_ordenados = [f"AT-{i:06d}" for i in range(100000)]
    alvo_procurado = "AT-087654"

    print("--- COMPARAÇÃO DE DESEMPENHO: BUSCA LINEAR VS BINÁRIA ---")

    # Medindo Busca Linear O(n)
    inicio = time.perf_counter()
    res_linear = busca_linear(ativos_ordenados, alvo_procurado)
    tempo_linear = (time.perf_counter() - inicio) * 1000

    # Medindo Busca Binária O(log n)
    inicio = time.perf_counter()
    res_binaria = busca_binaria(ativos_ordenados, alvo_procurado)
    tempo_binaria = (time.perf_counter() - inicio) * 1000

    print(f"Busca Linear (O(n)): Índice {res_linear} encontrado em {tempo_linear:.4f} ms")
    print(f"Busca Binária (O(log n)): Índice {res_binaria} encontrado em {tempo_binaria:.4f} ms")