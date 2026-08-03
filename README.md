<p align="center">
  <img src="assets/banner.svg" alt="Pokédex SQL Game" width="100%">
</p>

<p align="center">
  <img alt="python" src="https://img.shields.io/badge/python-3.11-4F9A4A?style=for-the-badge&logo=python&logoColor=white">
  <img alt="fastapi" src="https://img.shields.io/badge/backend-FastAPI-C0392B?style=for-the-badge&logo=fastapi&logoColor=white">
  <img alt="sqlite" src="https://img.shields.io/badge/data-SQLite-4A90D9?style=for-the-badge&logo=sqlite&logoColor=white">
  <img alt="status" src="https://img.shields.io/badge/status-em%20constru%C3%A7%C3%A3o-EF9F27?style=for-the-badge">
</p>

# 🔴 Pokédex SQL Game

Um Pokémon secreto é sorteado a cada partida. Em vez de clicar em botões,
você escreve **comandos SQL** pra descobrir as características dele,
comparar com outros Pokémon e arriscar um palpite — antes que o placar
zere. Projeto feito pra treinar SQL na prática, com uma cara de Pokédex.

<img src="assets/divider.svg" alt="" width="100%">

## 📖 Sobre o projeto

- 🎯 **Objetivo:** descobrir o nome do Pokémon secreto usando o mínimo
  possível de queries.
- 🖥️ **Interface:** simula uma Pokédex vermelha — a "tela" mostra o
  resultado das suas queries, e no lugar dos botões físicos tem um campo
  de SQL.
- 🧠 **Pra quem é:** qualquer pessoa aprendendo SQL que já sabe o básico
  de `SELECT`/`WHERE` e quer praticar `JOIN`, `GROUP BY` e subqueries de
  um jeito mais divertido que exercício de apostila.

## 🎮 Como o jogo funciona

1. Uma partida começa e um Pokémon é sorteado no banco — escondido de
   você.
2. Você escreve `SELECT`s contra views especiais (`mystery_pokemon`,
   `mystery_pokemon_stats`, etc.) pra descobrir características dele:
   tipo, altura, peso, stats, abilities, movimentos, linha evolutiva.
3. Você pode consultar livremente as tabelas normais do banco pra
   comparar — por exemplo, ver os stats de um Pokémon que você já
   conhece.
4. Quando tiver uma hipótese, arrisca um palpite com o nome.

## 🧮 Regras de pontuação

| Regra | Efeito |
|---|---|
| Placar inicial | **10 pontos** |
| Cada query contra o Pokémon secreto | **−1 ponto** |
| Cada tentativa de palpite (certa ou errada) | **−1 ponto** |
| Placar chega a 0 | 1 última chance de palpite ("sudden death") |
| Acertou o nome | 🏆 vitória |
| Errou a chance final | 💀 derrota — revela o Pokémon |

<img src="assets/divider.svg" alt="" width="100%">

## 🛠️ Stack tecnológica

| Camada | Tecnologia |
|---|---|
| Frontend | HTML + CSS + JS puro |
| Backend | Python + FastAPI |
| Banco de dados | SQLite ([veekun/pokedex](https://github.com/veekun/pokedex)) |
| Execução | Local, via GitHub Codespaces |

## 📂 Estrutura do projeto

```
pokedex-sql-game/
├── main.py               # roda tudo (comando: python main.py)
├── app/
│   ├── routes.py         # rotas /game/*
│   ├── db.py             # conexão e sessões SQLite
│   ├── game.py           # lógica de pontuação
│   ├── sql_guard.py      # validação de SQL do jogador
│   └── data/
│       └── pokedex.sqlite
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── assets/                # imagens deste README
├── requirements.txt
└── README.md
```

## 🚀 Como rodar

1. Abra este repositório em um **GitHub Codespace** (`Code` → `Codespaces`
   → `Create codespace on main`).
2. No terminal do Codespace, instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode o servidor:
   ```bash
   python main.py
   ```
4. Abra a aba **Ports** e clique no link de preview da porta encaminhada
   pelo Codespaces.

<img src="assets/divider.svg" alt="" width="100%">

## 🗺️ Roadmap

- [x] Escolher stack e desenhar a arquitetura
- [x] Especificar as regras do jogo e o schema das views secretas
- [ ] Criar as `mystery_*` views e validar contra o banco do veekun
- [ ] Endpoints básicos do FastAPI (`/game/start`, `/query`, `/guess`)
- [ ] Validação de segurança do SQL do jogador
- [ ] Frontend estático da Pokédex
- [ ] Integração frontend ↔ backend
- [ ] Polish visual e mensagens de erro

## 📜 Créditos

Dados de Pokémon vindos do projeto open-source
[veekun/pokedex](https://github.com/veekun/pokedex). Projeto feito com
fins educacionais, sem vínculo com a Nintendo/Game Freak.
