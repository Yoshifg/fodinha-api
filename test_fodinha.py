import pytest
from fodinha import Fodinha  # ajuste conforme o caminho real


@pytest.fixture
def jogo():
    jogo = Fodinha()
    jogo.adicionar_jogador("Murilo")
    jogo.adicionar_jogador("Juliana")
    jogo.adicionar_jogador("Yoshi")
    jogo.adicionar_jogador("Gu")
    jogo.iniciar_jogo()
    return jogo


def test_inicio_jogo(jogo):
    assert jogo.comecou is True
    assert jogo.rodada == 1
    assert all(len(j.cartas) == 1 for j in jogo.jogadores)


def test_primeira_rodada_mao_oculta(jogo):
    murilo_mao = jogo.get_mao("Murilo")
    assert "Murilo" not in murilo_mao
    assert set(murilo_mao.keys()) == {"Juliana", "Yoshi", "Gu"}


def test_palpite_binario(jogo):
    jogo.fazer_palpite("Murilo", 0)
    jogo.fazer_palpite("Juliana", 1)
    jogo.fazer_palpite("Yoshi", 0)
    jogo.fazer_palpite("Gu", 0)
    assert all(j.palpite in [0, 1] for j in jogo.jogadores)


def test_palpite_obrigatorio(jogo):
    jogo.fazer_palpite("Murilo", 0)
    jogo.fazer_palpite("Juliana", 0)
    jogo.fazer_palpite("Yoshi", 1)
    jogo.fazer_palpite("Gu", 0)
    assert sum(j.palpite for j in jogo.jogadores) == 2


def test_jogada_simples(jogo):
    for jogador in jogo.jogadores:
        jogo.fazer_palpite(jogador.nome, 1)
    primeira_vez = jogo.vez.nome
    jogo.fazer_jogada(primeira_vez)
    assert len(jogo.mesa) == 1


def test_empate_na_rodada(jogo):
    for jogador in jogo.jogadores:
        jogo.fazer_palpite(jogador.nome, 1)
    for jogador in jogo.jogadores:
        jogo.fazer_jogada(jogador.nome)
    assert jogo.jogador_vencedor_parcial is None
    assert jogo.carta_vencedora is None


def test_eliminacao_de_jogador():
    jogo = Fodinha()
    jogo.adicionar_jogador("A")
    jogo.adicionar_jogador("B")
    jogo.iniciar_jogo()

    for _ in range(3):
        for j in jogo.jogadores:
            jogo.fazer_palpite(j.nome, 0)
        for j in list(jogo.jogadores):  # cópia da lista original
            mao = jogo.get_mao(j.nome)
            if isinstance(mao, dict):  # primeira rodada
                carta = None
            else:
                carta = mao[0]
            jogo.fazer_jogada(j.nome, carta)

    assert len(jogo.jogadores) == 1
    assert jogo.comecou is False


def test_proxima_vez_rodando(jogo):
    for jogador in jogo.jogadores:
        jogo.fazer_palpite(jogador.nome, 1)
    atual = jogo.vez.nome
    jogo.fazer_jogada(atual)
    proximo = jogo.vez.nome
    assert proximo != atual


def test_get_estado_jogo(jogo):
    estado = jogo.get_estado_jogo()
    assert estado["rodada"] == 1
    assert len(estado["jogadores"]) == 4
    assert estado["vez"] in {"Murilo", "Juliana", "Yoshi", "Gu"}
