from flask import Flask, jsonify, request
from fodinha_game import Fodinha

import secrets, string

MAXIMO_JOGOS = 10  # Limite máximo de jogos

app = Flask(__name__)

jogos: dict[str, Fodinha] = {}  # Dicionário para armazenar os jogos pelos seus IDs


def _gerar_id(tamanho=6):
    caracteres = string.ascii_uppercase + string.digits  # A-Z, 0-9
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))


# Rota para criar um novo jogo
@app.route("/api/novo-jogo", methods=["POST"])
def novo_jogo():
    # Verifica se atingiu a quantidade maxima de jogos simultaneos
    if len(jogos) >= MAXIMO_JOGOS:
        return jsonify({"message": "Limite máximo de jogos atingido!"}), 403

    # Cria um novo jogo e armazena no dicionário
    while True:
        id_jogo = _gerar_id()
        if id_jogo not in jogos.keys():
            break

    jogo = Fodinha()
    jogos[id_jogo] = jogo
    return jsonify({"id": id_jogo, "message": "Novo jogo criado!"}), 201


# Rota para adicionar um jogador a um jogo existente
@app.route("/api/adicionar-jogador", methods=["POST"])
def adicionar_jogador():
    data = request.get_json()
    id_jogo = data.get("id_jogo")
    nome = data.get("nome")

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404
    if jogos[id_jogo].encontrar_jogador(nome):
        return jsonify({"message": "Jogador já adicionado!"}), 403

    # Adiciona o jogador ao jogo
    jogos[id_jogo].adicionar_jogador(nome)

    # Verifica se o jogador foi adicionado com sucesso
    if not jogos[id_jogo].encontrar_jogador(nome):
        return jsonify({"message": "Erro ao adicionar jogador!"}), 500

    return jsonify({"message": "Jogador adicionado com sucesso!"}), 201


# Rota para iniciar o jogo
@app.route("/api/iniciar-jogo", methods=["POST"])
def iniciar_jogo():
    data = request.get_json()
    id_jogo = data.get("id_jogo")

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404

    # Inicia o jogo
    jogos[id_jogo].iniciar_jogo()

    return jsonify({"message": "Jogo iniciado com sucesso!"}), 200

# Rota para um jogador fazer um palpite
@app.route("/api/fazer-palpite", methods=["POST"])
def fazer_palpite():
    data = request.get_json()
    id_jogo = data.get("id_jogo")
    nome = data.get("nome")
    palpite = data.get("palpite")

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404
    if not jogos[id_jogo].encontrar_jogador(nome):
        return jsonify({"message": "Jogador não encontrado!"}), 404

    # Faz o palpite
    try:
        jogos[id_jogo].fazer_palpite(nome, palpite)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Palpite registrado com sucesso!"}), 200

# Rota para fazer uma jogada
@app.route("/api/jogada", methods=["POST"])
def jogada():
    data = request.get_json()
    id_jogo = data.get("id_jogo")
    nome = data.get("nome")
    jogada = data.get("carta")

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404
    if not jogos[id_jogo].encontrar_jogador(nome):
        return jsonify({"message": "Jogador não encontrado!"}), 404

    # Faz a jogada
    try:
        jogos[id_jogo].fazer_jogada(nome, jogada)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Jogada registrada com sucesso!"}), 200

# Rota para obter o estado do jogo
@app.route("/api/estado-jogo", methods=["GET"])
def estado_jogo():
    id_jogo = request.args.get("id_jogo")

    if not id_jogo:
        return jsonify({"message": "ID do jogo não fornecido!"}), 400

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404

    # Retorna o estado do jogo
    estado = jogos[id_jogo].get_estado_jogo()
    return jsonify(estado), 200

# Rota para obter as cartas da mesa
@app.route("/api/mesa", methods=["GET"])
def pega_mesa():
    id_jogo = request.args.get("id_jogo")

    if not id_jogo:
        return jsonify({"message": "ID do jogo não fornecido!"}), 400

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404

    # Retorna o estado do jogo
    mesa = jogos[id_jogo].get_mesa()
    mesa["cartas"] = [str(carta) for carta, jogador in mesa["cartas"]]
    return jsonify(mesa), 200

# Rota para obter a mao de um jogador
@app.route("/api/mao", methods=["GET"])
def pega_mao():
    id_jogo = request.args.get("id_jogo")
    nome = request.args.get("nome")

    if not id_jogo:
        return jsonify({"message": "ID do jogo não fornecido!"}), 400

    if id_jogo not in jogos.keys():
        return jsonify({"message": "Jogo não encontrado!"}), 404
    
    if not jogos[id_jogo].encontrar_jogador(nome):
        return jsonify({"message": "Jogador não encontrado!"}), 404

    # Retorna o estado do jogo
    mao = jogos[id_jogo].get_mao(nome)
    return jsonify(str(mao)), 200


if __name__ == "__main__":
    app.run(debug=True)
