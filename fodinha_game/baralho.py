from functools import total_ordering


@total_ordering
class Carta:
    ORDEM_TRUCO = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
    NAIPES_ORDEM_MANILHA = {"P": 4, "C": 3, "E": 2, "O": 1}

    # Esta variável será configurada pelo jogo antes das comparações
    MANILHA = None  # Ex: '5'

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __str__(self):
        return f"{self.valor}{self.naipe}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def definir_manilha(cls, vira_valor):
        idx = cls.ORDEM_TRUCO.index(vira_valor)
        cls.MANILHA = cls.ORDEM_TRUCO[(idx + 1) % len(cls.ORDEM_TRUCO)]

    def is_manilha(self):
        return self.valor == Carta.MANILHA

    def ordem_valor(self):
        if self.valor not in Carta.ORDEM_TRUCO:
            return -1
        return Carta.ORDEM_TRUCO.index(self.valor)

    def __eq__(self, other):
        if not isinstance(other, Carta):
            return NotImplemented
        return self.__lt__(other) == False and other.__lt__(self) == False

    def __lt__(self, other):
        if not isinstance(other, Carta):
            return NotImplemented

        # Se uma das cartas é manilha, ela é maior
        if self.is_manilha() and not other.is_manilha():
            return False
        if not self.is_manilha() and other.is_manilha():
            return True
        if self.is_manilha() and other.is_manilha():
            return (
                Carta.NAIPES_ORDEM_MANILHA[self.naipe]
                < Carta.NAIPES_ORDEM_MANILHA[other.naipe]
            )

        # Se nenhuma é manilha, comparar pelo valor normal
        return self.ordem_valor() < other.ordem_valor()


class Baralho:
    def __init__(self):
        self.cartas = []

        for naipe in Carta.NAIPES_ORDEM_MANILHA.keys():
            for valor in Carta.ORDEM_TRUCO:
                self.cartas.append(Carta(valor, naipe))

        self.embaralhar()

    def embaralhar(self):
        import random

        random.shuffle(self.cartas)

    def pegar_carta(self):
        if self.cartas:
            return self.cartas.pop()
        else:
            return None

    def tamanho(self):
        return len(self.cartas)
