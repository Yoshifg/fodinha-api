import pytest
from app import app, jogos, MAXIMO_JOGOS
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Testa a criação de um novo jogo
@patch("app.Fodinha")
def test_criar_novo_jogo(mock_fodinha, client):
    jogos.clear()

    response = client.post("/api/novo-jogo")
    data = response.get_json()

    assert response.status_code == 201
    assert "id" in data
    assert data["message"] == "Novo jogo criado!"
    assert data["id"] in jogos


# Testa o limite máximo de jogos
@patch("app.Fodinha")
def test_limite_maximo_jogos(mock_fodinha, client):
    jogos.clear()
    for _ in range(MAXIMO_JOGOS):
        client.post("/api/novo-jogo")

    response = client.post("/api/novo-jogo")
    assert response.status_code == 403
    assert response.get_json()["message"] == "Limite máximo de jogos atingido!"


# Testa adicionar um jogador novo
@patch("app.Fodinha")
def test_adicionar_jogador(mock_fodinha_class, client):
    jogos.clear()
    mock_jogo = MagicMock()
    mock_jogo.encontrar_jogador.side_effect = [False, True]
    mock_fodinha_class.return_value = mock_jogo

    response = client.post("/api/novo-jogo")
    id_jogo = response.get_json()["id"]

    response = client.post(
        "/api/adiciona-jogador", json={"id_jogo": id_jogo, "nome": "Alice"}
    )
    print(response.get_json())
    assert response.status_code == 201
    assert response.get_json()["message"] == "Jogador adicionado com sucesso!"
    mock_jogo.adicionar_jogador.assert_called_with("Alice")


# Testa erro ao adicionar jogador repetido
@patch("app.Fodinha")
def test_adicionar_jogador_repetido(mock_fodinha_class, client):
    jogos.clear()
    mock_jogo = MagicMock()
    mock_jogo.encontrar_jogador.side_effect = [
        False,
        True,
        True
    ]  # Simula jogador sendo encontrado depois
    mock_fodinha_class.return_value = mock_jogo

    response = client.post("/api/novo-jogo")
    id_jogo = response.get_json()["id"]

    # Primeira adição
    client.post("/api/adiciona-jogador", json={"id_jogo": id_jogo, "nome": "Bob"})
    # Segunda tentativa
    response = client.post(
        "/api/adiciona-jogador", json={"id_jogo": id_jogo, "nome": "Bob"}
    )
    assert response.status_code == 403
    assert response.get_json()["message"] == "Jogador já adicionado!"


# Testa iniciar o jogo
@patch("app.Fodinha")
def test_iniciar_jogo(mock_fodinha_class, client):
    jogos.clear()
    mock_jogo = MagicMock()
    mock_fodinha_class.return_value = mock_jogo

    response = client.post("/api/novo-jogo")
    id_jogo = response.get_json()["id"]

    response = client.post("/api/iniciar-jogo", json={"id_jogo": id_jogo})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Jogo iniciado com sucesso!"
    mock_jogo.iniciar_jogo.assert_called_once()


# Testa obter estado do jogo
@patch("app.Fodinha")
def test_estado_jogo(mock_fodinha_class, client):
    jogos.clear()
    mock_jogo = MagicMock()
    mock_jogo.get_estado_jogo.return_value = {"status": "esperando jogadores"}
    mock_fodinha_class.return_value = mock_jogo

    response = client.post("/api/novo-jogo")
    id_jogo = response.get_json()["id"]

    response = client.get(f"/api/estado-jogo?id_jogo={id_jogo}")
    assert response.status_code == 200
    assert response.get_json()["status"] == "esperando jogadores"


# Testa obter estado do jogo com ID inválido
def test_estado_jogo_id_invalido(client):
    jogos.clear()
    response = client.get("/api/estado-jogo?id_jogo=INVALIDO")
    assert response.status_code == 404
    assert response.get_json()["message"] == "Jogo não encontrado!"


# Testa obter estado do jogo sem ID
def test_estado_jogo_sem_id(client):
    response = client.get("/api/estado-jogo")
    assert response.status_code == 400
    assert response.get_json()["message"] == "ID do jogo não fornecido!"
