from flask import Flask, jsonify, request
from fodinha_game import Fodinha

import secrets, string

MAXIMO_JOGOS = 10  # Limite máximo de jogos

app = Flask(__name__)

jogos: dict[str, Fodinha] = {}  # Dicionário para armazenar os jogos pelos seus IDs


# Sample route
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the Flask API!"})


def _gerar_id(tamanho=6):
    caracteres = string.ascii_uppercase + string.digits  # A-Z, 0-9
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))


# GET example
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


# POST example
@app.route("/api/adiciona-jogador", methods=["POST"])
def post_data():
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


if __name__ == "__main__":
    app.run(debug=True)
