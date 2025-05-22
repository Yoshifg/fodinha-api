# 📘 Documentação da API – Jogo Fodinha

Base URL: `http://localhost:5000/api`

---

## 🔧 POST `/novo-jogo`

**Cria um novo jogo de Fodinha.**

**Resposta de sucesso (201):**

```json
{
  "id": "ABC123",
  "message": "Novo jogo criado!"
}
```

**Erros:**

* `403`: Limite de jogos simultâneos atingido.

---

## 👤 POST `/adicionar-jogador`

**Adiciona um jogador a um jogo existente.**

**Body JSON:**

```json
{
  "id_jogo": "ABC123",
  "nome": "João"
}
```

**Respostas:**

* `201`: Jogador adicionado com sucesso.
* `403`: Jogador já adicionado.
* `404`: Jogo não encontrado.
* `500`: Falha ao adicionar jogador.

---

## ▶️ POST `/iniciar-jogo`

**Inicia a partida de um jogo existente.**

**Body JSON:**

```json
{
  "id_jogo": "ABC123"
}
```

**Respostas:**

* `200`: Jogo iniciado com sucesso.
* `404`: Jogo não encontrado.

---

## 🗣️ POST `/fazer-palpite`

**Envia um palpite para o jogador da vez.**

**Body JSON:**

```json
{
  "id_jogo": "ABC123",
  "nome": "João",
  "palpite": 2
}
```

**Respostas:**

* `200`: Palpite registrado com sucesso.
* `400`: Palpite inválido (fora do intervalo, fora da vez, etc.).
* `404`: Jogo ou jogador não encontrado.

---

## 🃏 POST `/jogada`

**Faz uma jogada com a carta escolhida.**

**Body JSON:**

```json
{
  "id_jogo": "ABC123",
  "nome": "João",
  "carta": "A♣"
}
```

> **Nota:** Na primeira rodada, a jogada é automática e não requer `carta`.

**Respostas:**

* `200`: Jogada registrada com sucesso.
* `400`: Carta inválida ou jogada fora da vez.
* `404`: Jogo ou jogador não encontrado.

---

## 📊 GET `/estado-jogo?id_jogo=ABC123`

**Retorna o estado completo do jogo.**

**Resposta de sucesso (200):**

```json
{
  "rodada": 2,
  "jogadores": [
    {
      "nome": "João",
      "vidas": 3,
      "palpite": 2,
      "ganhou": 1
    },
    ...
  ],
  "vez": "Maria",
  "vez_palpite": "João",
  "fase_palpite": true,
  "vencedor": null,
  "acabou": false
}
```

**Erros:**

* `400`: ID não fornecido.
* `404`: Jogo não encontrado.

---

## ♠️ GET `/mesa?id_jogo=ABC123`

**Retorna o estado atual da mesa.**

**Resposta de sucesso (200):**

```json
{
  "cartas": ["A♣", "Q♠"],
  "vencedora": "A♣",
  "fazendo": "João",
  "vira": "8♦"
}
```

**Erros:**

* `400`: ID não fornecido.
* `404`: Jogo não encontrado.

---

## ✋ GET `/mao?id_jogo=ABC123&nome=João`

**Retorna as cartas da mão do jogador especificado.**

> Na primeira rodada, o jogador **não vê sua própria carta**.

**Resposta (200):**

```json
["2♦", "J♠", "5♥"]
```

**Erros:**

* `400`: ID do jogo não fornecido.
* `404`: Jogo ou jogador não encontrado.

---