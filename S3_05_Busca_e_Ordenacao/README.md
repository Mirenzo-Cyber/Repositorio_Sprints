# S3_05 - Busca e Ordenação

Implementação prática de algoritmos clássicos de ordenação (`Bubble Sort`, `Selection Sort`, `Insertion Sort`) e de busca (`Busca Binária`) aplicados ao inventário de ativos de TI (Exercícios 1 a 7).

---

## Tabela Comparativa de Algoritmos (Exercícios 5 e 6)

| Algoritmo | Complexidade (Melhor Caso) | Complexidade (Pior Caso) | Vantagens | Limitações |
| :--- | :---: | :---: | :--- | :--- |
| **Bubble Sort** | O(n) | O(n^2) | Fácil de implementar; deteta listas já ordenadas. | Muito lento para volumes grandes de dados. |
| **Selection Sort** | O(n^2) | O(n^2) | Realiza menos trocas de memória que o Bubble Sort. | Número de comparações fixo e alto, independente da entrada. |
| **Insertion Sort** | O(n) | O(n^2) | Extremamente eficiente se a lista já estiver quase ordenada. | Lento para listas grandes totalmente desordenadas. |
| **Busca Binária** | O(1) | O(log n) | Incrivelmente rápida (divide o espaço de busca ao meio). | **Exige obrigatoriamente que a lista esteja ordenada.** |

---

## Análise de Desempenho (Exercício 5)
* Algoritmos de ordenação quadrática tornam-se inviáveis quando o número de ativos de TI cresce consideravelmente.
* Na prática de engenharia de software, utilizam-se algoritmos otimizados como o Timsort do `.sort()` nativo do Python em conjunto com a **Busca Binária** para recuperar dados de forma instantânea