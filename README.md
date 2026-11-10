# Repositório de Sprints e Trabalho 02

Repositório central de atividades práticas e projetos desenvolvidos ao longo das Sprints (Paradigmas de Programação, Estruturas de Dados, Análise de Algoritmos, Testes de Software, Álgebra Linear Aplicada e Desenvolvimento de APIs REST).

---

## 📁 Estrutura de Diretórios (Atividades das Sprints)

### Fundamentos, Estruturas de Dados e Algoritmos
* [S3_02 - Paradigmas de Programação: Funções de Alta Ordem e Recursão](./S3_02_Funcoes_Alta_Ordem_Recursao/)
* [S3_03 - Estruturas Lineares: Filas e Listas Encadeadas](./S3_03_Estruturas_Lineares/)
* [S3_04 - Análise de Algoritmos e Complexidade](./S3_04_Analise_Algoritmos_Complexidade/)
* [S3_05 - Busca e Ordenação](./S3_05_Busca_e_Ordenacao/)

### Engenharia de Software, Testes e Práticas Avançadas
* [S3_07 - Estratégias de Teste e Testes Unitários](./S3_07_Estrategias_de_Teste_e_Testes_Unitar/)
* [S3_08 - Atividade Prática de Git e GitHub](./S3_08---GITHUB-ACTIVITY-main/)
* [S3_12 - Atividades da Sprint 12](./S3_12/)
* [S3_16 - Atividades da Sprint 16](./S3_16/)
* [S3_17 - Atividades da Sprint 17](./S3_17/)
* [S3_18 - Atividades da Sprint 18](./S3_18/)
* [S3_19 - Atividades da Sprint 19](./S3_19/)
* [S3_20 - Atividades da Sprint 20](./S3_20/)

### Projeto Integrador
* [Trabalho 02 - Sistema de Inventário de Cibersegurança e Análise de Risco](./Trabalho_02/)

---

## 🛡️ Relatório Técnico: Trabalho 02 — Inventário e Análise de Risco

O projeto localizado no diretório `./Trabalho_02` consiste em um sistema completo para gestão de ativos de TI, mapeamento de vulnerabilidades e cálculo de propagação de risco em rede utilizando Álgebra Linear e uma API RESTful em Flask.

### 1. Programação Orientada a Objetos (POO), Herança e Polimorfismo
A base do sistema (`trabalho_02.py`) foi modelada utilizando classes para representar as entidades do domínio:
* **`Vulnerabilidade`**: Armazena o identificador (`id_vul`), descrição, categoria, severidade numérica baseada em CVSS e status.
* **`Equipamento` (Superclasse)**: Define os atributos comuns de cada ativo (`id_ativo`, `nome`, `responsavel`, `setor`, `tipo`), além da lista de vulnerabilidades associadas e um dicionário de dependências entre equipamentos.
* **Subclasses e Polimorfismo**: As classes filhas herdam de `Equipamento` e sobrescrevem o método `fator_exposicao()` para refletir a criticidade de cada categoria na infraestrutura:
  * `Computador`: fator $1.0$
  * `Notebook`: fator $1.2$
  * `Switch`: fator $1.3$
  * `Servidor`: fator $1.5$

### 2. Persistência de Dados em JSON
Para garantir que os cadastros não sejam perdidos ao encerrar a execução, a classe controladora `SistemaInventario` gerencia a leitura e gravação automática em arquivos locais:
* **`equipamentos.json`**: Armazena a lista serializada de todos os ativos, seus vínculos de vulnerabilidades e pesos de dependência.
* **`vulnerabilidades.json`**: Mantém o catálogo de vulnerabilidades cadastradas e suas respectivas notas de severidade.

### 3. Modelagem Matemática e Álgebra Linear (`NumPy`)
O cálculo de risco da infraestrutura utiliza matrizes e vetores construídos dinamicamente com a biblioteca `numpy`:

1. **Matriz de Incidência ($M$) e Vetor de Severidade ($v$)**:
   Para $n$ equipamentos e $m$ vulnerabilidades, a matriz $M$ de dimensão $n \times m$ recebe $1.0$ na posição $(i, j)$ caso o equipamento $i$ possua a vulnerabilidade $j$, e $0.0$ caso contrário. O vetor coluna $v$ de dimensão $m \times 1$ armazena as severidades.
2. **Vetor de Risco Próprio ($b$)**:
   Calculado pelo produto matricial entre $M$ e $v$, ponderado pelo vetor de fatores de exposição $f$ de cada equipamento:
   $$b = (M \cdot v) \odot f$$
3. **Matriz de Dependências ($A$) e Risco Total ($x$)**:
   A propagação de risco entre ativos é representada pela matriz quadrada $A$ de ordem $n \times n$, respeitando duas regras de validação:
   * Um equipamento não pode depender de si mesmo ($A_{ii} = 0$).
   * A soma das frações de risco na linha de qualquer equipamento deve ser estritamente menor que $1$ ($\sum_{k=1}^{n} A_{ik} < 1.0$), garantindo a convergência e invertibilidade do modelo.
   
   O vetor de Risco Total ($x$) é obtido resolvendo o sistema linear com a Matriz Identidade ($I$):
   $$(I - A)x = b$$

### 4. Arquitetura Web e API RESTful (`Flask`)
No arquivo `app.py`, as regras de negócio do `SistemaInventario` são expostas na web por meio de rotas HTTP que retornam dados estruturados em formato JSON:

| Método HTTP | Rota | Descrição | Códigos de Retorno |
| :--- | :--- | :--- | :--- |
| `GET` | `/equipamentos` | Lista todos os equipamentos cadastrados no inventário em formato JSON. | `200 OK` |
| `POST` | `/equipamentos` | Cadastra um novo equipamento a partir de um corpo JSON e atualiza o arquivo local. | `201 Created` / `400 Bad Request` |
| `GET` | `/risco` | Executa o cálculo matricial via `NumPy` e retorna o risco próprio e total de cada ativo. | `200 OK` / `400 Bad Request` |

---

## 🚀 Como Executar o Projeto (`Trabalho_02`)

Acesse a pasta do projeto pelo terminal antes de rodar os comandos para garantir que os arquivos `.json` sejam lidos corretamente:

```bash
cd Trabalho_02
```

### Opção 1: Iniciar o Servidor da API Web (Flask)
```bash
python app.py
```
O servidor ficará ativo em `http://127.0.0.1:5000`. As rotas podem ser testadas diretamente pelo navegador (para requisições `GET`) ou via Postman (para requisições `GET` e `POST`).

### Opção 2: Executar via Menu Interativo no Terminal
```bash
python trabalho_02.py
```
Abre o menu no console permitindo cadastrar ativos, associar vulnerabilidades, registrar dependências e visualizar a tabela de risco diretamente no terminal.