import sys

# Força o terminal a ler e escrever em UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')

import json
import numpy as np

# --- ETAPA 1: CLASSES (Orientação a Objetos, Herança e Polimorfismo) ---
class Vulnerabilidade:
    def __init__(self, id_vul, descricao, categoria, severidade, status="Aberta"):
        self.id_vul = int(id_vul)
        self.descricao = descricao
        self.categoria = categoria
        self.severidade = float(severidade)  # Valor numérico para o vetor v
        self.status = status

    def to_dict(self):
        return self.__dict__


class Equipamento:
    def __init__(self, id_ativo, nome, responsavel, setor, tipo):
        self.id_ativo = int(id_ativo)
        self.nome = nome
        self.responsavel = responsavel
        self.setor = setor
        self.tipo = tipo
        self.vulnerabilidades_ids = []  # IDs das vulnerabilidades associadas (Matriz M)
        self.dependencias = {}          # {"id_alvo": fracao_risco} (Matriz A)

    # Polimorfismo: cada classe derivada sobrescreve o seu fator de exposição
    def fator_exposicao(self):
        return 1.0

    def to_dict(self):
        return {
            "id_ativo": self.id_ativo,
            "nome": self.nome,
            "responsavel": self.responsavel,
            "setor": self.setor,
            "tipo": self.tipo,
            "vulnerabilidades_ids": self.vulnerabilidades_ids,
            "dependencias": self.dependencias
        }


# Subclasses com polimorfismo aplicado às categorias
class Computador(Equipamento):
    def fator_exposicao(self):
        return 1.0


class Notebook(Equipamento):
    def fator_exposicao(self):
        return 1.2


class Servidor(Equipamento):
    def fator_exposicao(self):
        return 1.5


class Switch(Equipamento):
    def fator_exposicao(self):
        return 1.3


# --- ETAPAS 2 e 3: GESTÃO DO SISTEMA, JSON, CADASTROS E DEPENDÊNCIAS ---
class SistemaInventario:
    def __init__(self):
        self.equipamentos = {}      # id_ativo -> Objeto Equipamento
        self.vulnerabilidades = {}  # id_vul -> Objeto Vulnerabilidade
        self.carregar_dados()

    def criar_objeto_equipamento(self, id_ativo, nome, responsavel, setor, tipo):
        mapa_classes = {
            "COMPUTADORES": Computador,
            "NOTEBOOKS": Notebook,
            "SERVIDORES": Servidor,
            "SWITCHES": Switch
        }
        classe_escolhida = mapa_classes.get(tipo, Equipamento)
        return classe_escolhida(id_ativo, nome, responsavel, setor, tipo)

    def salvar_dados(self):
        # Requisito 2: Persistência em listas de objetos JSON
        with open("equipamentos.json", "w", encoding="utf-8") as f:
            lista_eq = [eq.to_dict() for eq in self.equipamentos.values()]
            json.dump(lista_eq, f, indent=4, ensure_ascii=False)

        with open("vulnerabilidades.json", "w", encoding="utf-8") as f:
            lista_vul = [vul.to_dict() for vul in self.vulnerabilidades.values()]
            json.dump(lista_vul, f, indent=4, ensure_ascii=False)

    def carregar_dados(self):
        try:
            with open("equipamentos.json", "r", encoding="utf-8") as f:
                for d in json.load(f):
                    eq = self.criar_objeto_equipamento(
                        d["id_ativo"], d["nome"], d["responsavel"], d["setor"], d["tipo"]
                    )
                    eq.vulnerabilidades_ids = d.get("vulnerabilidades_ids", [])
                    eq.dependencias = d.get("dependencias", {})
                    self.equipamentos[eq.id_ativo] = eq
        except FileNotFoundError:
            pass

        try:
            with open("vulnerabilidades.json", "r", encoding="utf-8") as f:
                for d in json.load(f):
                    vul = Vulnerabilidade(
                        d["id_vul"], d["descricao"], d["categoria"], d["severidade"], d.get("status", "Aberta")
                    )
                    self.vulnerabilidades[vul.id_vul] = vul
        except FileNotFoundError:
            pass

    def cadastrar_ativo(self):
        print("\n--- Cadastro de Novo Equipamento ---")
        try:
            id_ativo = int(input("ID do equipamento (apenas números): "))
            if id_ativo in self.equipamentos:
                print("Erro: ID já cadastrado.")
                return

            nome = input("Nome: ").strip()
            resp = input("Responsável: ").strip()
            setor = input("Setor: ").strip()

            print("Categorias disponíveis: 1. COMPUTADORES | 2. NOTEBOOKS | 3. SERVIDORES | 4. SWITCHES")
            opcoes = {1: "COMPUTADORES", 2: "NOTEBOOKS", 3: "SERVIDORES", 4: "SWITCHES"}
            tipo = opcoes.get(int(input("Escolha o número da categoria: ")))

            if not tipo or not nome:
                print("Erro: Dados inválidos.")
                return

            novo_eq = self.criar_objeto_equipamento(id_ativo, nome, resp, setor, tipo)
            self.equipamentos[id_ativo] = novo_eq
            self.salvar_dados()
            print(f"Equipamento '{nome}' registado e guardado em JSON com sucesso!")
        except ValueError:
            print("Erro: Entrada inválida.")

    def cadastrar_vulnerabilidade(self):
        print("\n--- Cadastrar e Associar Vulnerabilidade ---")
        try:
            id_vul = int(input("ID da Vulnerabilidade (apenas números): "))
            if id_vul not in self.vulnerabilidades:
                desc = input("Descrição da vulnerabilidade: ").strip()
                cat = input("Categoria (ex: Software desatualizado, Senha fraca): ").strip()
                sev = float(input("Severidade numérica CVSS (ex: 7.5): "))
                self.vulnerabilidades[id_vul] = Vulnerabilidade(id_vul, desc, cat, sev)
            else:
                print(f"Vulnerabilidade existente selecionada: {self.vulnerabilidades[id_vul].descricao}")

            id_eq = int(input("ID do Equipamento afetado por esta vulnerabilidade: "))
            if id_eq in self.equipamentos:
                if id_vul not in self.equipamentos[id_eq].vulnerabilidades_ids:
                    self.equipamentos[id_eq].vulnerabilidades_ids.append(id_vul)
                    self.salvar_dados()
                    print("Vulnerabilidade associada e guardada no ficheiro JSON!")
                else:
                    print("Aviso: O equipamento já possui esta vulnerabilidade associada.")
            else:
                print("Erro: Equipamento não encontrado.")
        except ValueError:
            print("Erro: Insira valores numéricos válidos para IDs e Severidade.")

    def cadastrar_dependencia(self):
        print("\n--- Cadastrar Dependência entre Equipamentos ---")
        try:
            id_origem = int(input("ID do equipamento dependente (o que recebe o risco): "))
            if id_origem not in self.equipamentos:
                print("Erro: Equipamento dependente não encontrado.")
                return

            id_destino = int(input("ID do equipamento do qual depende (origem do risco): "))
            if id_destino not in self.equipamentos:
                print("Erro: Equipamento de destino não encontrado.")
                return

            # Regra: Um ativo não pode depender de si mesmo (A_ii = 0)
            if id_origem == id_destino:
                print("Erro: Um equipamento não pode depender de si mesmo (A_ii deve ser 0).")
                return

            peso = float(input("Fração de risco transmitida (ex: 0.25 para 25%): "))
            if peso <= 0 or peso >= 1:
                print("Erro: A fração deve estar entre 0 e 1 (exclusivo).")
                return

            eq = self.equipamentos[id_origem]

            # Soma das dependências já cadastradas na linha deste equipamento
            soma_atual = sum(float(v) for k, v in eq.dependencias.items() if k != str(id_destino))

            # Regra: A soma dos elementos da linha de A deve ser < 1 para garantir invertibilidade
            if soma_atual + peso >= 1.0:
                print(f"Erro: A soma das dependências ficaria em {soma_atual + peso:.2f}.")
                print("Regra violada: A soma da linha em A deve ser estritamente menor que 1.0.")
                return

            eq.dependencias[str(id_destino)] = peso
            self.salvar_dados()
            print(f"Sucesso: Equipamento {id_origem} agora herda {peso * 100:.1f}% do risco do Equipamento {id_destino}!")
        except ValueError:
            print("Erro: Entrada inválida. Introduza números válidos.")

    def listar_ativos(self):
        print("\n--- Lista de Equipamentos Cadastrados ---")
        if not self.equipamentos:
            print("Nenhum equipamento cadastrado.")
            return

        for eq in self.equipamentos.values():
            print(f"\n[ID: {eq.id_ativo}] {eq.nome} | Tipo: {eq.tipo} | Fator Exposição: {eq.fator_exposicao()}")
            print(f"  Responsável: {eq.responsavel} | Setor: {eq.setor}")
            print(f"  Vulnerabilidades (IDs): {eq.vulnerabilidades_ids if eq.vulnerabilidades_ids else 'Nenhuma'}")
            
            if eq.dependencias:
                deps_formatadas = [f"Ativo {alvo} ({peso * 100:.1f}%)" for alvo, peso in eq.dependencias.items()]
                print(f"  Depende de: {', '.join(deps_formatadas)}")
            else:
                print("  Depende de: Nenhuma dependência registada.")

    def calcular_analise_risco(self):
        print("\n--- Analise de Risco com Algebra Linear ---")
        
        lista_eq = list(self.equipamentos.values())
        lista_vul = list(self.vulnerabilidades.values())
        
        n = len(lista_eq)
        m = len(lista_vul)
        
        if n == 0 or m == 0:
            print("Erro: É necessário ter pelo menos um equipamento e uma vulnerabilidade cadastrados.")
            return

        # "Tradutores" de ID real para posição na matriz
        mapa_idx_eq = {eq.id_ativo: i for i, eq in enumerate(lista_eq)}
        mapa_idx_vul = {vul.id_vul: j for j, vul in enumerate(lista_vul)}

        # Inicialização de M e v
        M = np.zeros((n, m), dtype=np.float64)
        v = np.zeros((m, 1), dtype=np.float64)
        
        # Preenchimento do placar (vetor v)
        for j, vul in enumerate(lista_vul):
            v[j, 0] = vul.severidade

        # Preenchimento do tabuleiro (Matriz M)
        for i, eq in enumerate(lista_eq):
            for id_vul in eq.vulnerabilidades_ids:
                if id_vul in mapa_idx_vul:
                    j = mapa_idx_vul[id_vul]
                    M[i, j] = 1.0

        # Fatores de exposição e Risco Próprio (b)
        fatores = np.array([eq.fator_exposicao() for eq in lista_eq]).reshape(-1, 1)
        b = (M @ v) * fatores

        # Inicializa e preenche a Matriz de Dependências A (n por n)
        A = np.zeros((n, n), dtype=np.float64)
        for i, eq in enumerate(lista_eq):
            for id_destino_str, peso in eq.dependencias.items():
                id_destino = int(id_destino_str)
                if id_destino in mapa_idx_eq:
                    k = mapa_idx_eq[id_destino]
                    A[i, k] = float(peso)

        # Cálculo do Risco Total (x) resolvendo (I - A)x = b
        I = np.eye(n, dtype=np.float64)
        x = np.linalg.solve(I - A, b)

        # Exibição do Relatório de Risco
        print(f"\n{'ID':<5} | {'Equipamento':<20} | {'Risco Proprio (b)':<18} | {'Risco Total (x)'}")
        print("-" * 65)
        for i, eq in enumerate(lista_eq):
            risco_proprio = b[i, 0]
            risco_total = x[i, 0]
            print(f"{eq.id_ativo:<5} | {eq.nome:<20} | {risco_proprio:<18.2f} | {risco_total:.2f}")
                    

# --- MENU PRINCIPAL ---
sistema = SistemaInventario()

while True:
    print("\n--- Sistema de Inventario e Analise de Risco ---")
    print("1. Cadastrar Equipamento")
    print("2. Cadastrar / Associar Vulnerabilidade")
    print("3. Cadastrar Dependência entre Equipamentos")
    print("4. Listar Equipamentos e Dependências")
    print("5. Calcular Análise de Risco")
    print("6. Sair")

    opcao = input("Escolha uma opção (1 a 6): ").strip()

    if opcao == "1":
        sistema.cadastrar_ativo()
    elif opcao == "2":
        sistema.cadastrar_vulnerabilidade()
    elif opcao == "3":
        sistema.cadastrar_dependencia()
    elif opcao == "4":
        sistema.listar_ativos()
    elif opcao == "5":
        sistema.calcular_analise_risco()
    elif opcao == "6":
        print("\nA encerrar o sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")