import sqlite3
import uuid

DB_PATH = "app/data/pokedex.sqlite"

# sessões ativas: session_id -> dict com a conexão e o estado da partida
sessions = {}

MYSTERY_VIEWS_SQL = """
CREATE TEMP VIEW mystery_pokemon AS
SELECT
    p.height,
    p.weight,
    sp.generation_id AS generation,
    (SELECT t.identifier FROM pokemon_types pt JOIN types t ON t.id = pt.type_id
     WHERE pt.pokemon_id = p.id AND pt.slot = 1) AS type_1,
    (SELECT t.identifier FROM pokemon_types pt JOIN types t ON t.id = pt.type_id
     WHERE pt.pokemon_id = p.id AND pt.slot = 2) AS type_2,
    (SELECT COUNT(*) FROM pokemon_species s2
     WHERE s2.evolution_chain_id = sp.evolution_chain_id) AS evolution_chain_length
FROM pokemon p
JOIN pokemon_species sp ON sp.id = p.species_id
WHERE p.id = {secret_id};

CREATE TEMP VIEW mystery_pokemon_stats AS
SELECT s.identifier AS stat_name, ps.base_stat AS base_value
FROM pokemon_stats ps
JOIN stats s ON s.id = ps.stat_id
WHERE ps.pokemon_id = {secret_id};

CREATE TEMP VIEW mystery_pokemon_abilities AS
SELECT a.identifier AS ability_name
FROM pokemon_abilities pa
JOIN abilities a ON a.id = pa.ability_id
WHERE pa.pokemon_id = {secret_id};

CREATE TEMP VIEW mystery_pokemon_moves AS
SELECT DISTINCT m.identifier AS move_name, pmm.identifier AS learn_method
FROM pokemon_moves pm
JOIN moves m ON m.id = pm.move_id
JOIN pokemon_move_methods pmm ON pmm.id = pm.pokemon_move_method_id
WHERE pm.pokemon_id = {secret_id};
"""


def _pick_random_pokemon_id(conn):
    cur = conn.execute(
        "SELECT id FROM pokemon WHERE is_default = 1 AND id <= 721 "
        "ORDER BY RANDOM() LIMIT 1"
    )
    return cur.fetchone()[0]


def create_session():
    """Cria uma nova partida: abre conexão somente leitura, sorteia um
    pokémon e cria as mystery views escondidas nessa conexão."""
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, check_same_thread=False)

    secret_id = _pick_random_pokemon_id(conn)
    name_row = conn.execute(
        "SELECT sp.identifier FROM pokemon p "
        "JOIN pokemon_species sp ON sp.id = p.species_id "
        "WHERE p.id = ?",
        (secret_id,),
    ).fetchone()
    secret_name = name_row[0]

    conn.executescript(MYSTERY_VIEWS_SQL.format(secret_id=secret_id))

    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "conn": conn,
        "secret_id": secret_id,
        "secret_name": secret_name,
        "score": 10,
        "sudden_death": False,
        "game_over": False,
    }
    return session_id, sessions[session_id]


def get_session(session_id):
    if session_id not in sessions:
        raise KeyError("sessão não encontrada")
    return sessions[session_id]
