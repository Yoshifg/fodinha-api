from fodinha import Fodinha


def test_eliminacao_de_jogador():
    jogo = Fodinha()
    jogo.adicionar_jogador("A")
    jogo.adicionar_jogador("B")
    jogo.iniciar_jogo()

    jogo.fazer_palpite("A", 0)
    jogo.fazer_palpite("B", 0)

    print(jogo.jogadores)
    print(jogo.vira)
    jogo.fazer_jogada("A")
    jogo.fazer_jogada("B")

    print(jogo.jogadores[0])
    print(jogo.jogadores[1])


if __name__ == "__main__":
    test_eliminacao_de_jogador()
    print("Teste de eliminação de jogador passou!")
