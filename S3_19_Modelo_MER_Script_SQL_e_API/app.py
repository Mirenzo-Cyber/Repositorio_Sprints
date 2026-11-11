# Importamos o Flask para criar nossa API e request para pegar os dados enviados
from flask import Flask, request, jsonify
# Importamos sqlite3 para trabalhar com banco de dados relacional (SQL)
import sqlite3
# Importamos numpy para fazer cálculos matemáticos e matriciais de avaliação de risco
import numpy as np

# Inicializa o nosso aplicativo (API)
app = Flask(__name__)

# Classe orientada a objetos para gerenciar o banco de dados
class GerenciadorBanco:
    def __init__(self, nome_banco='inventario.db'):
        # Define o nome do arquivo do banco de dados onde os dados serão salvos
        self.nome_banco = nome_banco

    def conectar(self):
        # Cria ou abre a conexão com o banco de dados
        conexao = sqlite3.connect(self.nome_banco)
        # Permite acessar os dados retornados pelos nomes das colunas
        conexao.row_factory = sqlite3.Row
        return conexao

    def inicializar_tabelas(self):
        # Passo 2: Executar Script SQL para criar as tabelas
        conexao = self.conectar()
        cursor = conexao.cursor()
        
        # Script SQL: Cria a tabela de Ativos (Nossos computadores)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ativos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                ip TEXT NOT NULL,
                criticidade INTEGER NOT NULL
            )
        ''')
        
        # Script SQL: Cria a tabela de Vulnerabilidades (Com chave estrangeira)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ativo_id INTEGER,
                descricao TEXT NOT NULL,
                risco REAL NOT NULL,
                FOREIGN KEY (ativo_id) REFERENCES ativos(id)
            )
        ''')
        
        # Salva as alterações no banco e fecha a conexão
        conexao.commit()
        conexao.close()

# Cria uma instância (objeto) do nosso gerenciador de banco
db = GerenciadorBanco()


# ==========================================
# Passo 3, 4 e 5: Implementação do CRUD
# ==========================================

# Rota para CADASTRAR um novo ativo (Letra 'C' do CRUD - Create)
@app.route('/ativos', methods=['POST'])
def criar_ativo():
    # Recebe os dados em formato JSON (Ex: do Postman)
    dados = request.get_json()
    
    conexao = db.conectar()
    cursor = conexao.cursor()
    
    # Comando SQL INSERT para salvar no banco de dados (Persistência)
    cursor.execute(
        'INSERT INTO ativos (nome, ip, criticidade) VALUES (?, ?, ?)',
        (dados['nome'], dados['ip'], dados['criticidade'])
    )
    conexao.commit()
    conexao.close()
    
    # Devolve um aviso de sucesso para quem chamou a API
    return jsonify({"mensagem": "Ativo criado com sucesso no banco de dados!"}), 201

# Rota para LER todos os ativos (Letra 'R' do CRUD - Read / Consulta SQL)
@app.route('/ativos', methods=['GET'])
def listar_ativos():
    conexao = db.conectar()
    cursor = conexao.cursor()
    
    # Comando SQL SELECT para buscar todos os dados armazenados
    cursor.execute('SELECT * FROM ativos')
    ativos = cursor.fetchall()
    conexao.close()
    
    # Transforma os dados em uma lista de dicionários para exibir na tela do Postman
    lista_ativos = [dict(ativo) for ativo in ativos]
    return jsonify(lista_ativos), 200

# Rota para ATUALIZAR um ativo (Letra 'U' do CRUD - Update)
@app.route('/ativos/<int:id_ativo>', methods=['PUT'])
def atualizar_ativo(id_ativo):
    # Recebe as novas informações
    dados = request.get_json()
    
    conexao = db.conectar()
    cursor = conexao.cursor()
    
    # Comando SQL UPDATE para mudar os dados de um ativo específico
    cursor.execute(
        'UPDATE ativos SET nome = ?, ip = ?, criticidade = ? WHERE id = ?',
        (dados['nome'], dados['ip'], dados['criticidade'], id_ativo)
    )
    conexao.commit()
    conexao.close()
    
    return jsonify({"mensagem": "Ativo atualizado com sucesso!"}), 200

# Rota para APAGAR um ativo (Letra 'D' do CRUD - Delete)
@app.route('/ativos/<int:id_ativo>', methods=['DELETE'])
def deletar_ativo(id_ativo):
    conexao = db.conectar()
    cursor = conexao.cursor()
    
    # Comando SQL DELETE para remover definitivamente do banco
    cursor.execute('DELETE FROM ativos WHERE id = ?', (id_ativo,))
    conexao.commit()
    conexao.close()
    
    return jsonify({"mensagem": "Ativo deletado com sucesso!"}), 200

# ==========================================
# Integração Avançada: Avaliação de Risco 
# ==========================================

# Rota para calcular o risco do ativo usando matrizes do NumPy
@app.route('/ativos/<int:ativo_id>/analise-risco', methods=['GET'])
def analise_risco(ativo_id):
    conexao = db.conectar()
    cursor = conexao.cursor()
    
    # Consulta SQL filtrando pela Chave Estrangeira
    cursor.execute('SELECT risco FROM vulnerabilidades WHERE ativo_id = ?', (ativo_id,))
    resultados = cursor.fetchall()
    conexao.close()
    
    # Se o ativo não tiver vulnerabilidades, avisa o usuário
    if not resultados:
        return jsonify({"mensagem": "Este ativo não possui vulnerabilidades cadastradas."}), 404
        
    # Extrai apenas os números de risco da consulta
    lista_riscos = [linha['risco'] for linha in resultados]
    
    # Usa o NumPy para transformar a lista em matriz e fazer o cálculo matemático
    matriz_riscos = np.array(lista_riscos)
    risco_medio = np.mean(matriz_riscos)
    
    return jsonify({
        "ativo_id": ativo_id,
        "risco_medio_numpy": float(risco_medio)
    }), 200

# Ponto de partida do nosso programa
if __name__ == '__main__':
    # Primeiro garantimos que as tabelas existem (Passo 2 e Validação da Persistência)
    db.inicializar_tabelas()
    # Roda o nosso servidor Flask para aceitar as requisições (modo debug ligado)
    app.run(debug=True)