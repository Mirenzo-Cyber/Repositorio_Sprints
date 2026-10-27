# S3_02 - Funções de Alta Ordem e Recursão

Trabalho prático aplicando recursão, memoização e funções de alta ordem (`map`, `filter` e `lambda`) em Python, usando como base o inventário de ativos de TI e Cibersegurança.

## Arquivos do projeto

* **`recursao_desempenho.py`**: Testes de Fatorial (iterativo vs. recursivo) e Fibonacci (com e sem memoização), medindo o tempo de execução.
* **`alta_ordem_ativos.py`**: Uso de `map()`, `filter()` e `sorted()` com `lambda` para manipular os ativos de TI.
* **`ativos.txt`**: Lista dos equipamentos cadastrados e suas vulnerabilidades.

---

## Comparação de Desempenho (Exercícios 1, 2 e 3)

Tempos medidos no terminal em milissegundos (ms):

### 1. Fatorial (`n = 500`)
* **Iterativo:** `0.09500 ms`
* **Recursivo:** `0.15850 ms`

**O que aconteceu:** O modo iterativo foi mais rápido porque usa apenas um laço `for` simples. O recursivo demora um pouco mais porque o Python precisa empilhar 500 chamadas da função na memória antes de devolver o resultado.

### 2. Fibonacci (`n = 32` | Resultado: `2178309`)
* **Sem Memoização:** `623.18530 ms`
* **Com Memoização:** `0.02380 ms`

**O que aconteceu:** Sem memoização, a função recalcula os mesmos valores milhões de vezes, o que deixa o código lento (mais de meio segundo). Com memoização, salvamos os valores já calculados em um dicionário (cache), deixando o cálculo quase instantâneo.

---

## Funções de Alta Ordem nos Ativos (Exercícios 4, 5 e 6)

* **`map()` (Exercício 4):** Conta quantas vulnerabilidades cada equipamento tem e adiciona o status de risco (`CRÍTICO`, `ATENÇÃO` ou `SEGURO`).
* **`filter()` (Exercício 5):** Filtra o dicionário para mostrar apenas os equipamentos da categoria `Servidores`.
* **`lambda` + `sorted()` (Exercício 6):** Ordena os ativos do mais vulnerável para o mais seguro, ajudando a ver quais máquinas precisam de correção primeiro.