# Importa as ferramentas do Flask para construir a API web
# jsonify: converte listas e dicionários Python para o formato JSON
# request: captura os dados enviados nas requisições (ex: via Postman)
from flask import Flask, jsonify, request

# Importa a classe principal onde está a lógica do inventário
from trabalho_02 import SistemaInventario

# Inicializa a aplicação Flask
app = Flask(__name__)

# Instancia o sistema para carregar os dados dos arquivos JSON na memória
sistema = SistemaInventario()

# --- ROTA 1: Listar Equipamentos (GET = buscar/ler dados) ---
@app.route('/equipamentos', methods=['GET'])
def obter_equipamentos():
    # Converte todos os equipamentos salvos na memória para o formato de dicionário
    lista_equipamentos = [eq.to_dict() for eq in sistema.equipamentos.values()]
    
    # Retorna a lista em JSON com o código 200 (OK / Sucesso)
    return jsonify(lista_equipamentos), 200

# --- ROTA 2: Cadastrar Novo Equipamento (POST = enviar/criar dados) ---
@app.route('/equipamentos', methods=['POST'])
def criar_equipamento():
    # Captura o pacote JSON enviado no corpo da requisição
    dados = request.json
    
    # Extrai as informações de cada campo recebido
    id_ativo = dados.get('id_ativo')
    nome = dados.get('nome')
    responsavel = dados.get('responsavel')
    setor = dados.get('setor')
    tipo = dados.get('tipo')

    # Verifica se o ID já existe para evitar cadastros duplicados
    if id_ativo in sistema.equipamentos:
        # Retorna erro 400 (Requisição Inválida)
        return jsonify({"erro": "ID do equipamento já existe."}), 400

    # Instancia o equipamento na subclasse correta aplicando o polimorfismo
    novo_eq = sistema.criar_objeto_equipamento(id_ativo, nome, responsavel, setor, tipo)
    
    # Salva no dicionário da memória e atualiza o arquivo equipamentos.json
    sistema.equipamentos[id_ativo] = novo_eq
    sistema.salvar_dados()

    # Retorna mensagem de confirmação com o código 201 (Criado)
    return jsonify({"mensagem": f"Equipamento '{nome}' cadastrado com sucesso!"}), 201

# --- ROTA 3: Calcular Risco Total com NumPy ---
@app.route('/risco', methods=['GET'])
def relatorio_risco():
    # Chama o método que faz o cálculo matricial e devolve os dados estruturados
    resultados = sistema.calcular_analise_risco_api()
    
    # Se faltar equipamento ou vulnerabilidade, retorna a mensagem de erro com código 400
    if isinstance(resultados, dict) and "erro" in resultados:
        return jsonify(resultados), 400
        
    # Retorna o relatório final de risco em JSON com código 200 (OK)
    return jsonify(resultados), 200

# Garante que o servidor só inicie quando este arquivo for executado diretamente
if __name__ == '__main__':
    # debug=True reinicia o servidor automaticamente ao salvar alterações no código
    app.run(debug=True, port=5000)