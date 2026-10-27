import time
from functools import lru_cache

# ==========================================
# 1. Calculo Fatorial: Iterativo vs Recursivo
# ==========================================
def fatorial_iterativo(n):
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado

def fatorial_recursivo(n):
    if n <= 1:
        return 1
    return n * fatorial_recursivo(n - 1)

# ==========================================
# 2. Fibonacci: Sem Memoização vs Com Memoização
# ==========================================
def fibonacci_sem_memo(n):
    if n <= 1:
        return n
    return fibonacci_sem_memo(n - 1) + fibonacci_sem_memo(n - 2)

# Opção A: Memoização manual usando dicionário
def fibonacci_memo_manual(n, cache=None):
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fibonacci_memo_manual(n - 1, cache) + fibonacci_memo_manual(n - 2, cache)
    return cache[n]

# Opção B: Memoização nativa do Python com decorador (alta ordem!)
@lru_cache(maxsize=None)
def fibonacci_com_lru(n):
    if n <= 1:
        return n
    return fibonacci_com_lru(n - 1) + fibonacci_com_lru(n - 2)


# ==========================================
# 3. Comparação de Desempenho
# ==========================================
def medir_tempo(funcao, *args):
    inicio = time.perf_counter()
    resultado = funcao(*args)
    fim = time.perf_counter()
    tempo_ms = (fim - inicio) * 1000
    return resultado, tempo_ms

if __name__ == "__main__":
    print("--- COMPARAÇÃO: FATORIAL (n = 500) ---")
    _, t_fat_iter = medir_tempo(fatorial_iterativo, 500)
    _, t_fat_rec = medir_tempo(fatorial_recursivo, 500)
    print(f"Iterativo: {t_fat_iter:.5f} ms | Recursivo: {t_fat_rec:.5f} ms\n")

    print("--- COMPARAÇÃO: FIBONACCI (n = 32) ---")
    res_fib1, t_fib_sem = medir_tempo(fibonacci_sem_memo, 32)
    res_fib2, t_fib_com = medir_tempo(fibonacci_memo_manual, 32)
    print(f"Resultado: {res_fib1}")
    print(f"Sem Memoização: {t_fib_sem:.5f} ms")
    print(f"Com Memoização: {t_fib_com:.5f} ms")