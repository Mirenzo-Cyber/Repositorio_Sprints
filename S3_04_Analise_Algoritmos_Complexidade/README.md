# S3_04 - Análise de Algoritmos e Complexidade

Relatório técnico contendo a análise assintótica, comparação de algoritmos de busca e o estudo de custos de estruturas de dados aplicadas ao inventário de ativos de TI (Exercícios 1 a 5).

---

## 1. Identificação de Complexidade de Trechos em Python (Exercícios 1 e 4)

* **Exemplo A (Acesso Direto a Dicionário / Hash):**
  ```python
  ativo = inventario_ti["AT-001"]  # O(1)