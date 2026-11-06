import time
from collections import deque

# ==========================================
# 1. Fila utilizando lista padrão do Python (list)
# ==========================================
class FilaLista:
    def __init__(self):
        self.itens = []

    def enfileirar(self, chamado):
        self.itens.append(chamado)  # O(1)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.itens.pop(0)  # O(n) -> desloca todos os outros elementos!
        return None

    def esta_vazia(self):
        return len(self.itens) == 0

# ==========================================
# 2. Fila utilizando collections.deque
# ==========================================
class FilaDeque:
    def __init__(self):
        self.itens = deque()

    def enfileirar(self, chamado):
        self.itens.append(chamado)  # O(1)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.itens.popleft()  # O(1) -> remoção instantânea na ponta!
        return None

    def esta_vazia(self):
        return len(self.itens) == 0

# ==========================================
# Exemplos de Uso e Comparação Prática
# ==========================================
if __name__ == "__main__":
    chamados_seguranca = [
        "[AT-001] SRV-DB-PROD: Corrigir Porta 22 exposta",
        "[AT-004] PC-FIN-12: Desativar SMB v1",
        "[AT-002] SW-CORE-01: Alterar comunidade SNMP padrão",
        "[AT-005] SRV-WEB-APP: Configurar Headers HTTP"
    ]

    print("--- 1. FILA COM LISTA PYTHON (FIFO) ---")
    fila_lista = FilaLista()
    for c in chamados_seguranca:
        fila_lista.enfileirar(c)

    while not fila_lista.esta_vazia():
        print(f"Atendendo -> {fila_lista.desenfileirar()}")

    print("\n--- 2. FILA COM COLLECTIONS.DEQUE (FIFO) ---")
    fila_deque = FilaDeque()
    for c in chamados_seguranca:
        fila_deque.enfileirar(c)

    while not fila_deque.esta_vazia():
        print(f"Atendendo -> {fila_deque.desenfileirar()}")

    # Teste rápido de desempenho com 20.000 itens para provar a diferença O(n) vs O(1)
    N = 20000
    for i in range(N):
        fila_lista.enfileirar(i)
        fila_deque.enfileirar(i)

    inicio = time.perf_counter()
    while not fila_lista.esta_vazia():
        fila_lista.desenfileirar()
    t_lista = (time.perf_counter() - inicio) * 1000

    inicio = time.perf_counter()
    while not fila_deque.esta_vazia():
        fila_deque.desenfileirar()
    t_deque = (time.perf_counter() - inicio) * 1000

    print(f"\n--- COMPARAÇÃO DE DESEMPENHO (Removendo {N} itens) ---")
    print(f"Fila com list (pop(0) - O(n)): {t_lista:.4f} ms")
    print(f"Fila com deque (popleft() - O(1)): {t_deque:.4f} ms")