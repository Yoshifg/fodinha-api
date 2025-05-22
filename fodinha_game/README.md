## 📘 Documentação de Uso – Classe `Fodinha`

A classe `Fodinha` implementa a lógica do jogo de cartas "Fodinha", permitindo gerenciar jogadores, rodadas, palpites, jogadas e acompanhar o estado do jogo.

---

### ✅ **1. Inicialização**

```python
from jogo import Fodinha

jogo = Fodinha()
```

---

### 👥 **2. Adicionando Jogadores**

Adicione de 2 a 4 jogadores antes de iniciar o jogo.

```python
jogo.adicionar_jogador("Alice")
jogo.adicionar_jogador("Bob")
```

---

### 🕹️ **3. Iniciar o Jogo**

Inicia o jogo e distribui as cartas da primeira rodada.

```python
jogo.iniciar_jogo()
```

---

### 🔮 **4. Fazer Palpites**

Cada jogador faz seu palpite em ordem, sobre quantas rodadas pretende ganhar.
Use:

```python
jogo.fazer_palpite("Alice", 1)
```

---

### 🃏 **5. Jogar Cartas**

Depois dos palpites, os jogadores jogam suas cartas em ordem:

```python
jogo.fazer_jogada("Alice", carta_objeto)
```

> ⚠️ Na **primeira rodada**, o jogador joga automaticamente a única carta que tem (sem saber qual é), então `carta_objeto` deve ser omitido.

---

### 📊 **6. Consultar Estado do Jogo**

#### Ver o estado geral:

```python
jogo.get_estado_jogo()
```

#### Ver cartas na mesa:

```python
jogo.get_mesa()
```

#### Ver a carta "vira" (definidora da manilha):

```python
jogo.get_vira()
```

#### Ver a mão de um jogador:

```python
jogo.get_mao("Bob")
```

---

### ⚔️ **7. Regras Internas Importantes**

* Cada jogador começa com **3 vidas**.
* Perde vidas se o número de vitórias for diferente do palpite.
* Jogadores são eliminados quando ficam com 0 vidas.
* O jogo termina automaticamente quando sobrar apenas 1 jogador.

---

### 🧪 Exemplo Completo

```python
jogo = Fodinha()
jogo.adicionar_jogador("Ana")
jogo.adicionar_jogador("Beto")
jogo.iniciar_jogo()

jogo.fazer_palpite("Ana", 1)
jogo.fazer_palpite("Beto", 0)

mao = jogo.get_mao("Ana")
jogo.fazer_jogada("Ana", mao[0])
```
Aqui está a **documentação das rotas** da sua API Flask para o jogo Fodinha, pronta para ser usada como `docs.md`, incluída no `README.md` ou até como base para gerar documentação Swagger/OpenAPI futuramente:

---