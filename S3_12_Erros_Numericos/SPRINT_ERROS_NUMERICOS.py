from decimal import Decimal

print("\n=== 2. Erro Absoluto e Relativo ===")
valor_exato = float(Decimal('0.3'))
valor_aprox = 0.1 + 0.2

erro_absoluto = abs(valor_exato - valor_aprox)
erro_relativo = erro_absoluto / valor_exato

print(f"Valor Exato:      {valor_exato}")
print(f"Valor Aproximado: {valor_aprox}")
print(f"Erro Absoluto:    {erro_absoluto:.20e}")
print(f"Erro Relativo:    {erro_relativo:.20e}")


import math

print("\n=== 3. Truncamento vs. Arredondamento ===")
numero = 3.14159
casas = 4

# Arredondamento
arredondado = round(numero, casas)

# Truncamento 
fator = 10 ** casas # 10000
truncado = math.trunc(numero * fator) / fator

erro_arredondamento = abs(numero - arredondado)
erro_truncamento = abs(numero - truncado)

print(f"Original:    {numero}")
print(f"Arredondado: {arredondado} | Erro Absoluto: {erro_arredondamento:.6f}")
print(f"Truncado:    {truncado} | Erro Absoluto: {erro_truncamento:.6f}")

print("\n=== 4. Efeitos de Precisão Limitada ===")
grande = 1e16
pequeno = 1.0

soma_absorvida = grande + pequeno
print(f"Grande: {grande}")
print(f"Pequeno: {pequeno}")
print(f"1e16 + 1.0 == 1e16? {soma_absorvida == grande}")
print(f"Resultado de (1e16 + 1.0) - 1e16: {(grande + pequeno) - grande}")

print("\n=== 5. Propagação de Erros em Cálculos Sucessivos ===")
iteracoes = 100000
passo = 0.1
acumulador = 0.0

for _ in range(iteracoes):
    acumulador += passo

esperado = iteracoes * 0.1 # 10000.0
erro_acumulado = abs(esperado - acumulador)

print(f"Valor Esperado: {esperado}")
print(f"Valor Obtido:   {acumulador:.10f}")
print(f"Erro Acumulado: {erro_acumulado:.10e}")


import numpy as np
import math

print("\n=== 6. Utilizar Numpy para análise numérica básica ===")
# Criar um vetor com 100.000 elementos iguais a 0.1
vetor = np.full(100000, 0.1, dtype=np.float64)
soma_numpy = np.sum(vetor)
erro_numpy = abs(10000.0 - soma_numpy)

print(f"Soma com np.sum(): {soma_numpy:.10f}")
print(f"Erro com NumPy:    {erro_numpy:.10e}")

print("\n=== 7. Comparar valores com == e com tolerância (isclose) ===")
a = 0.1 + 0.2
b = 0.3

print(f"Comparação com '==':         {a == b}")
print(f"Comparação com math.isclose: {math.isclose(a, b)}")


import numpy as np

print("\n=== 8. Determinante vs. Número de Condição ===")
# Matriz quase singular genérica
A = np.array([
    [1.0, 1.0],
    [1.0, 1.00000001]
], dtype=np.float64)

b = np.array([2.0, 2.00000001], dtype=np.float64)

det_A = np.linalg.det(A)
cond_A = np.linalg.cond(A)

print(f"Determinante de A:       {det_A:.10e}")
print(f"Número de Condição de A: {cond_A:.10e}")

print("\n=== 9. Resolução do Sistema: solve vs. inv ===")
# Método 1: numpy.linalg.solve (Direto)
x_solve = np.linalg.solve(A, b)
residuo_solve = np.linalg.norm(A @ x_solve - b)

# Método 2: numpy.linalg.inv (Inversão explícita)
A_inv = np.linalg.inv(A)
x_inv = A_inv @ b
residuo_inv = np.linalg.norm(A @ x_inv - b)

print(f"[solve] Resíduo ||Ax - b||: {residuo_solve:.10e}")
print(f"[inv]   Resíduo ||Ax - b||: {residuo_inv:.10e}")