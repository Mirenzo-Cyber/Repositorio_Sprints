# ==========================================
# 3. Implementação da Lista Encadeada Simples
# ==========================================
class No:
    """Representa cada nó (elemento) da lista encadeada."""
    def __init__(self, id_ativo, nome, tipo):
        self.id_ativo = id_ativo
        self.nome = nome
        self.tipo = tipo
        self.proximo = None  # Ponteiro para o próximo nó

class ListaEncadeadaAtivos:
    def __init__(self):
        self.cabeca = None  # Início da lista (Head)

    # ==========================================
    # 4. Operações de Inserção e Remoção
    # ==========================================
    def inserir_no_inicio(self, id_ativo, nome, tipo):
        """Inserção no início em tempo constante O(1)."""
        novo_no = No(id_ativo, nome, tipo)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def inserir_no_fim(self, id_ativo, nome, tipo):
        """Inserção no final percorrendo a lista O(n)."""
        novo_no = No(id_ativo, nome, tipo)
        if not self.cabeca:
            self.cabeca = novo_no
            return
        atual = self.cabeca
        while atual.proximo:
            atual = atual.proximo
        atual.proximo = novo_no

    def remover_ativo(self, id_ativo):
        """Busca e remove um ativo pelo ID O(n)."""
        atual = self.cabeca
        anterior = None

        while atual:
            if atual.id_ativo == id_ativo:
                if anterior is None:
                    # O nó a remover é o primeiro (cabeça)
                    self.cabeca = atual.proximo
                else:
                    # Liga o nó anterior diretamente ao próximo
                    anterior.proximo = atual.proximo
                print(f"[REMOÇÃO] Ativo {id_ativo} ({atual.nome}) removido com sucesso.")
                return True
            anterior = atual
            atual = atual.proximo

        print(f"[AVISO] Ativo {id_ativo} não encontrado na lista.")
        return False

    # ==========================================
    # 5. Percorrer todos os elementos da lista
    # ==========================================
    def percorrer_lista(self):
        """Percorre e exibe todos os nós da lista encadeada O(n)."""
        atual = self.cabeca
        if not atual:
            print("A lista encadeada está vazia.")
            return

        caminho = []
        while atual:
            caminho.append(f"[{atual.id_ativo}: {atual.nome}]")
            atual = atual.proximo
        caminho.append("None")
        print(" -> ".join(caminho))

# ==========================================
# Exemplo de Uso
# ==========================================
if __name__ == "__main__":
    lista = ListaEncadeadaAtivos()

    print("--- 4. INSERINDO ATIVOS NA LISTA ENCADEADA ---")
    lista.inserir_no_fim("AT-001", "SRV-DB-PROD", "Servidores")
    lista.inserir_no_fim("AT-002", "SW-CORE-01", "Switches")
    lista.inserir_no_fim("AT-003", "NB-SEC-04", "Notebooks")
    lista.inserir_no_inicio("AT-000", "FW-BORDA-01", "Firewall (Prioridade)")

    print("\n--- 5. PERCORRENDO A LISTA ENCADEADA ---")
    lista.percorrer_lista()

    print("\n--- 4. REMOVENDO UM ATIVO (AT-002) E PERCORRENDO NOVAMENTE ---")
    lista.remover_ativo("AT-002")
    lista.percorrer_lista()