# 🛡️ Relatório Técnico: Redes, Segurança, LGPD e Sustentabilidade

> **Projeto:** Sistema de Inventário de Cibersegurança - Trabalho 02
> **Sprint:** [S3_20]

---

## 📡 1. Mecanismos de Comunicação da Aplicação

A arquitetura do sistema baseia-se no padrão **REST** (Representational State Transfer), operando localmente (`127.0.0.1:5000`). 

* **Protocolo Base:** A comunicação é feita via **HTTP**.
* **Formato de Dados:** Todas as trocas de informação entre o cliente (Postman) e a API (Flask) utilizam o formato **JSON**, garantindo leveza e legibilidade na transmissão.
* **Semântica de Rotas (CRUD):** 
  * `POST` para criação de novos ativos.
  * `GET` para leitura e consulta de informações.
  * `PUT` para atualização de dados existentes.
  * `DELETE` para remoção de registros.

---

## 🔐 2. Controle de Acesso (Menor Privilégio)

Para proteger os endpoints da API, a proposta de controle de acesso adota o **Princípio do Menor Privilégio**, dividindo as permissões da seguinte forma:

* **🛠️ Administrador de Redes:** Acesso total (CRUD). É o único perfil com permissão para utilizar `POST`, `PUT` e `DELETE` na rota `/ativos`, podendo alterar a infraestrutura do banco.
* **🔎 Analista de Segurança:** Acesso restrito à leitura. Pode utilizar apenas `GET` em `/ativos` e acessar `/analise-risco` para monitorar vulnerabilidades, sem qualquer permissão de alteração.
* **📊 Auditor Externo:** Acesso de leitura estritamente a dados anonimizados e relatórios estatísticos, sem capacidade de visualizar IPs ou dados críticos.

---

## ⚖️ 3. Requisitos de Proteção de Dados (LGPD)

O sistema foi projetado respeitando as diretrizes da Lei Geral de Proteção de Dados Pessoais (LGPD):

* **Identificação de Dados:** O **Endereço IP** armazenado na tabela `ativos` é tratado como dado pessoal/sensível, uma vez que pode ser associado ao comportamento de um funcionário específico em sua estação de trabalho.
* **Princípio da Minimização:** O banco de dados coleta e retém *apenas* os dados essenciais para o escopo de cibersegurança (Nome, IP, Criticidade, Risco). Não são coletados dados supérfluos (como nomes de usuários) sem justificativa legal.
* **Rastreabilidade (Logs):** Em um ambiente de produção, todos os acessos à API gerariam *logs* seguros para auditoria, cujo acesso também seria rigorosamente controlado sob as regras da LGPD.

---

## 📈 4. Análise Estatística Simples dos Dados

Com a integração da biblioteca **NumPy**, a aplicação consegue extrair inteligência dos dados coletados de forma altamente otimizada:

* **Média de Risco:** A rota `/analise-risco` aplica a função `np.mean()` nas notas de vulnerabilidade cadastradas, entregando imediatamente o nível central de exposição de um equipamento.
* **Moda de Criticidade:** Identifica qual a classificação de importância mais comum na rede (níveis 1, 2 ou 3), orientando onde o orçamento de TI deve ser priorizado.
* **Mediana e Desvio Padrão:** Em análises futuras, permitem entender a distribuição das falhas, evitando que uma única vulnerabilidade com nota extrema distorça a avaliação geral de segurança da rede.

---

## 🌱 5. Sustentabilidade em Sistemas Computacionais

A arquitetura do projeto foi estruturada para minimizar o impacto ambiental, alinhando-se aos conceitos de *Green IT*:

* **Eficiência de Processamento:** O uso do **NumPy** (cujas operações matriciais rodam em C) reduz os ciclos de CPU em comparação com laços `for` tradicionais no Python, resultando em menor consumo elétrico do servidor.
* **Armazenamento Otimizado:** A escolha do **SQLite** como banco relacional elimina a necessidade de manter um motor de banco de dados pesado consumindo memória RAM e energia continuamente em *background*.
* **