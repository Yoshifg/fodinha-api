from baralho import Baralho, Carta


class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.cartas = []
        self.palpite = None
        self.palpite_acumulado = 0
        self.rodadas_ganhas = 0

    def receber_cartas(self, cartas):
        self.cartas = cartas

    def jogar_carta(self, carta):
        if carta not in self.cartas:
            raise ValueError("Jogador não possui essa carta.")
        self.cartas.remove(carta)
        return carta

    def vidas_restantes(self):
        return max(0, 3 - abs(self.palpite_acumulado - self.rodadas_ganhas))

    def reset_rodada(self):
        self.palpite_acumulado += self.palpite or 0
        self.cartas = []
        self.palpite = None

    def __repr__(self):
        return f"Jogador({self.nome}, Vidas: {self.vidas_restantes()}, Cartas: {self.cartas})"


class Fodinha:
    def __init__(self):
        self.jogadores: list[Jogador] = []
        self.maximo_jogadores = 4
        self.maximo_cartas = 5
        self.baralho = Baralho()
        self.comecou = False
        self.rodada = 0

        self.vira: Carta | None = None
        self.vez: Jogador | None = None
        self.vez_palpite: Jogador | None = None
        self.fase_palpite = True

        self.mesa = []
        self.carta_vencedora = None
        self.jogador_vencedor_parcial = None
        self.ultimo_vencedor = None

    # --- Setup do Jogo ---
    def adicionar_jogador(self, nome):
        if len(self.jogadores) >= self.maximo_jogadores:
            raise ValueError("Máximo de jogadores atingido.")
        self.jogadores.append(Jogador(nome))

    def iniciar_jogo(self):
        if len(self.jogadores) < 2:
            raise ValueError("Número mínimo de jogadores não atingido.")
        self.comecou = True
        self.rodada = 1
        self._nova_rodada()

    def _nova_rodada(self):
        for jogador in self.jogadores:
            jogador.reset_rodada()

        # Alternância de quem começa o palpite
        if self.vez_palpite is not None:
            self._proximo_jogador_palpite()
        else:
            self.vez_palpite = self.jogadores[0]

        self.baralho = Baralho()
        self.baralho.embaralhar()
        self.vira = self.baralho.pegar_carta()
        Carta.definir_manilha(self.vira.valor)  # type: ignore

        num_cartas = self._num_cartas_rodada()
        for jogador in self.jogadores:
            jogador.receber_cartas(
                [self.baralho.pegar_carta() for _ in range(num_cartas)]
            )

        self.mesa = []
        self.fase_palpite = True
        self.vez = self.vez_palpite

    def _num_cartas_rodada(self):
        crescente = list(range(1, self.maximo_cartas + 1))
        decrescente = list(range(self.maximo_cartas - 1, 0, -1))
        sequencia = crescente + decrescente
        idx = (self.rodada - 1) % len(sequencia)
        return sequencia[idx]

    # --- Palpites ---
    def fazer_palpite(self, nome_jogador, palpite):
        if self.vez_palpite.nome != nome_jogador:  # type: ignore
            raise ValueError("Não é a vez do jogador fazer palpite.")

        jogador = self._encontrar_jogador(nome_jogador)

        if not self.fase_palpite:
            raise ValueError("Não é fase de palpite.")

        if jogador.palpite is not None:
            raise ValueError("Palpite já feito.")

        if self.rodada == 1:
            if palpite not in [0, 1]:
                raise ValueError("Na primeira rodada, palpite deve ser 0 ou 1.")
            jogador.palpite = palpite

            if all(j.palpite is not None for j in self.jogadores):
                # Regra especial da primeira rodada
                num_fazem = sum(j.palpite for j in self.jogadores if j.palpite)
                if num_fazem == 1 and jogador.palpite == 0:
                    jogador.palpite = 1  # type: ignore
                self.fase_palpite = True

        else:
            palpites = [
                j.palpite if j.nome != nome_jogador and j.palpite is not None else 0
                for j in self.jogadores
            ]
            total = sum(palpites) + palpite

            if (
                len([j for j in self.jogadores if j.palpite is not None])
                == len(self.jogadores) - 1
            ):
                if total == self._num_cartas_rodada():
                    raise ValueError(
                        "Soma dos palpites não pode ser igual ao número de cartas."
                    )

            jogador.palpite = palpite

        if all(j.palpite is not None for j in self.jogadores):
            self.fase_palpite = False

        self._proximo_jogador_palpite()

    def _proximo_jogador_palpite(self):
        idx = self.jogadores.index(self.vez_palpite)  # type: ignore
        self.vez_palpite = self.jogadores[(idx + 1) % len(self.jogadores)]

    # --- Jogadas ---
    def fazer_jogada(self, nome_jogador, carta=None):
        if self.fase_palpite:
            raise ValueError("Ainda estamos na fase de palpites.")

        jogador = self._encontrar_jogador(nome_jogador)
        if jogador != self.vez:
            raise ValueError("Não é a vez do jogador.")

        if self.rodada == 1:
            if len(jogador.cartas) != 1:
                raise ValueError(
                    "Jogador deve ter exatamente uma carta na primeira rodada."
                )
            carta_jogada = jogador.cartas.pop()
        else:
            if carta is None:
                raise ValueError("Você precisa informar qual carta jogar.")
            carta_jogada = jogador.jogar_carta(carta)

        self.mesa.append((carta_jogada, jogador))

        # Verifica se há vencedor parcial
        if self.carta_vencedora is None:
            self.carta_vencedora = carta_jogada
            self.jogador_vencedor_parcial = jogador
        else:
            if carta_jogada > self.carta_vencedora:
                self.carta_vencedora = carta_jogada
                self.jogador_vencedor_parcial = jogador
            elif carta_jogada == self.carta_vencedora:
                self.carta_vencedora = None
                self.jogador_vencedor_parcial = None

        if len(self.mesa) == len(self.jogadores):
            self._resolver_rodada()
        else:
            self._proximo_jogador()

    def _resolver_rodada(self):
        if self.jogador_vencedor_parcial:
            self.jogador_vencedor_parcial.rodadas_ganhas += 1
            self.vez = self.jogador_vencedor_parcial
            self.ultimo_vencedor = self.jogador_vencedor_parcial
        else:
            print("Rodada empatada. Nenhum jogador venceu.")

        self.mesa = []
        self.carta_vencedora = None
        self.jogador_vencedor_parcial = None

        if all(len(j.cartas) == 0 for j in self.jogadores):
            self._remover_jogadores_eliminados()

            if self.vez not in self.jogadores:
                self.vez = self.jogadores[0] if self.jogadores else None

            if len(self.jogadores) == 1:
                print(f"Fim de jogo! {self.jogadores[0].nome} venceu!")
                self.comecou = False
                return

            self.rodada += 1
            self._nova_rodada()

    def _proximo_jogador(self):
        idx = self.jogadores.index(self.vez)  # type: ignore
        self.vez = self.jogadores[(idx + 1) % len(self.jogadores)]

    def _remover_jogadores_eliminados(self):
        self.jogadores = [j for j in self.jogadores if j.vidas_restantes() > 0]

    # --- Utilitários ---
    def _encontrar_jogador(self, nome):
        for j in self.jogadores:
            if j.nome == nome:
                return j
        raise ValueError("Jogador não encontrado.")

    # --- Estado do Jogo ---
    def get_mao(self, nome_jogador):
        jogador = self._encontrar_jogador(nome_jogador)
        if self.rodada == 1:
            return {j.nome: j.cartas for j in self.jogadores if j != jogador}
        return jogador.cartas

    def get_vira(self):
        return self.vira

    def get_mesa(self):
        return {
            "cartas": [(repr(carta), jogador.nome) for carta, jogador in self.mesa],
            "vencedora": repr(self.carta_vencedora) if self.carta_vencedora else None,
            "fazendo": (
                self.jogador_vencedor_parcial.nome
                if self.jogador_vencedor_parcial
                else None
            ),
        }

    def get_estado_jogo(self):
        return {
            "rodada": self.rodada,
            "jogadores": [
                {
                    "nome": j.nome,
                    "vidas": j.vidas_restantes(),
                    "palpite": j.palpite,
                    "ganhou": j.rodadas_ganhas,
                }
                for j in self.jogadores
            ],
            "vez": self.vez.nome if self.vez else None,
            "vez_palpite": self.vez_palpite.nome if self.vez_palpite else None,
            "fase_palpite": self.fase_palpite,
        }
