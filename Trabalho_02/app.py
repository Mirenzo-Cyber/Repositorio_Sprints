# Importamos as ferramentas do Flask para criar a API web
# jsonify: Transforma dicionários Python em texto JSON para a internet
# request: Permite capturar os dados que o utilizador envia para a nossa API
from flask import Flask, jsonify, request

# Importamos a classe principal do trabalho que já testámos e validámos
from trabalho_02 import SistemaInventario

# Inicializa a nossa aplicação web (API) com o nome do ficheiro atual
app = Flask(__name__)

# Instancia o sistema para carregar os dados dos ficheiros JSON existentes
sistema = SistemaInventario()

# --- ROTA 1: Listar Equipamentos (Método GET = Pedir/Ler dados) ---
@app.route('/equipamentos', methods=['GET'])
def obter_equipamentos():
    # Pegamos todos os equipamentos guardados na memória
    lista_equipamentos = [eq.to_dict() for eq in sistema.equipamentos.values()]
    
    # Devolvemos a lista no formato JSON com o código de sucesso 200 (OK)
    return jsonify(lista_equipamentos), 200

# --- ROTA 2: Cadastrar Novo Equipamento (Método POST = Enviar/Criar dados) ---
@app.route('/equipamentos', methods=['POST'])
def criar_equipamento():
    # Capturamos o pacote de dados JSON enviado (por exemplo, via Postman)
    dados = request.json
    
    # Extraímos as informações enviadas no corpo da requisição
    id_ativo = dados.get('id_ativo')
    nome = dados.get('nome')
    responsavel = dados.get('responsavel')
    setor = dados.get('setor')
    tipo = dados.get('tipo')

    # Verificamos se o equipamento já existe para não duplicar
    if id_ativo in sistema.equipamentos:
        return jsonify({"erro": "ID do equipamento já existe."}), 400

    # Usamos a função de polimorfismo que já criaste para gerar a classe correta
    novo_eq = sistema.criar_objeto_equipamento(id_ativo, nome, responsavel, setor, tipo)
    
    # Guardamos na memória e atualizamos o ficheiro equipamentos.json
    sistema.equipamentos[id_ativo] = novo_eq
    sistema.salvar_dados()

    # Retornamos uma mensagem de sucesso com o código 201 (Created/Criado)
    return jsonify({"mensagem": f"Equipamento '{nome}' cadastrado com sucesso!"}), 201

# --- ROTA 3: Calcular Risco Total com NumPy ---
@app.route('/risco', methods=['GET'])
def relatorio_risco():
    # Como a função original imprime no terminal, precisamos adaptar a lógica 
    # ou simplesmente chamar a função (ela fará os cálculos e atualizará os objetos)
    # Por agora, vamos retornar uma mensagem simples para confirmar que a rota funciona
    return jsonify({"mensagem": "Rota de cálculo de risco da Matriz Acessada."}), 200

# Este bloco garante que o servidor só liga se rodarmos este ficheiro diretamente
if __name__ == '__main__':
    # O modo debug=True recarrega o servidor automaticamente quando guardamos o ficheiro
    app.run(debug=True, port=5000)