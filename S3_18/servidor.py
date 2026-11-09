# Importamos o Flask e as ferramentas para lidar com JSON e requisições
from flask import Flask, jsonify, request

# Passo 1: Criamos o nosso aplicativo (servidor) Flask
app = Flask(__name__)

# Simulando um banco de dados com uma lista de dicionários (os seus ativos)
ativos = [
    {"id": 1, "nome": "Servidor de Banco de Dados", "categoria": "Hardware", "nivelRisco": "Alto"},
    {"id": 2, "nome": "Firewall Principal", "categoria": "Rede", "nivelRisco": "Médio"}
]

# Passo 2: Rota GET para listar todos os ativos
@app.route('/api/ativos', methods=['GET'])
def listar_ativos():
    # Transforma a lista do Python em JSON e envia com o código 200 (OK)
    return jsonify(ativos), 200

# Passo 3: Rota POST para adicionar um novo ativo
@app.route('/api/ativos', methods=['POST'])
def criar_ativo():
    # Pega os dados em JSON enviados no corpo (Body) da requisição
    novo_ativo = request.get_json()
    
    # Cria um ID novo baseado no tamanho da lista e adiciona o ativo
    novo_ativo['id'] = len(ativos) + 1
    ativos.append(novo_ativo)
    
    # Retorna o ativo criado e o código 201 (Created)
    return jsonify(novo_ativo), 201

# Passo 4: Rota PUT para atualizar um ativo existente pelo seu ID
# O <int:id> captura o número que vem no final da URL (ex: /api/ativos/1)
@app.route('/api/ativos/<int:id>', methods=['PUT'])
def atualizar_ativo(id):
    # Pega os novos dados que você enviou pelo Postman
    dados_atualizados = request.get_json()
    
    # Usa um laço de repetição (for) para procurar o ativo com o ID correspondente
    for ativo in ativos:
        if ativo['id'] == id:
            # Se encontrar o ID, atualiza as informações com os dados novos
            ativo['nome'] = dados_atualizados.get('nome', ativo['nome'])
            ativo['categoria'] = dados_atualizados.get('categoria', ativo['categoria'])
            ativo['nivelRisco'] = dados_atualizados.get('nivelRisco', ativo['nivelRisco'])
            
            # Devolve o ativo atualizado e o código 200 (OK) que o Postman espera
            return jsonify(ativo), 200
            
    # Se o laço terminar e não achar o ID, devolve erro 404 (Não Encontrado)
    return jsonify({"erro": "Ativo não encontrado"}), 404

# Passo 5: Rota DELETE para remover um ativo pelo seu ID
@app.route('/api/ativos/<int:id>', methods=['DELETE'])
def deletar_ativo(id):
    # Procura o ativo na lista usando o ID recebido na URL
    for ativo in ativos:
        if ativo['id'] == id:
            # Remove o ativo encontrado da nossa lista
            ativos.remove(ativo)
            
            # Devolve uma resposta vazia ('') e o código 204 (No Content / Sem Conteúdo)
            # É exatamente esse código 204 que faz o teste 4 do seu Postman passar!
            return '', 204
            
    # Se tentar apagar um ID que não existe, devolve erro 404 (Não Encontrado)
    return jsonify({"erro": "Ativo não encontrado"}), 404

# Passo 6: Comando padrão para ligar o servidor quando executamos o arquivo
if __name__ == '__main__':
    # Roda o servidor localmente na porta 5000 com reinício automático ativado
    app.run(debug=True, port=5000)