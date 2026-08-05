from . import db
from .sql_guard import validate_select

MYSTERY_TABLES = (
    "mystery_pokemon_stats",
    "mystery_pokemon_abilities",
    "mystery_pokemon_moves",
    "mystery_pokemon",
)


def start_game():
    session_id, session = db.create_session()
    return {
        "session_id": session_id,
        "score": session["score"],
        "sudden_death": session["sudden_death"],
    }


def run_query(session_id: str, sql: str):
    session = db.get_session(session_id)

    if session["game_over"]:
        return {"error": "o jogo já acabou, comece uma nova partida", "score": session["score"]}

    try:
        clean_sql = validate_select(sql)
    except ValueError as e:
        return {"error": str(e), "score": session["score"]}

    touches_mystery = any(t in clean_sql.lower() for t in MYSTERY_TABLES)

    try:
        cur = session["conn"].execute(clean_sql)
        rows = cur.fetchall()
        columns = [d[0] for d in cur.description] if cur.description else []
    except Exception as e:
        return {"error": f"erro no SQL: {e}", "score": session["score"]}

    if touches_mystery:
        _spend_point(session)

    return {
        "columns": columns,
        "rows": rows,
        "score": session["score"],
        "sudden_death": session["sudden_death"],
        "game_over": session["game_over"],
    }


def make_guess(session_id: str, name: str):
    session = db.get_session(session_id)

    if session["game_over"]:
        return {"error": "o jogo já acabou, comece uma nova partida", "score": session["score"]}

    correct = name.strip().lower() == session["secret_name"].lower()

    if correct:
        session["game_over"] = True
        return {
            "correct": True,
            "score": session["score"],
            "sudden_death": session["sudden_death"],
            "game_over": True,
            "message": f"você acertou! era o {session['secret_name']}",
        }

    was_sudden_death = session["sudden_death"]
    _spend_point(session)

    if was_sudden_death:
        session["game_over"] = True
        return {
            "correct": False,
            "score": session["score"],
            "sudden_death": True,
            "game_over": True,
            "message": f"errou a chance final! era o {session['secret_name']}",
        }

    return {
        "correct": False,
        "score": session["score"],
        "sudden_death": session["sudden_death"],
        "game_over": False,
        "message": "errado, tente de novo",
    }


def _spend_point(session):
    if session["sudden_death"]:
        return
    session["score"] -= 1
    if session["score"] <= 0:
        session["score"] = 0
        session["sudden_death"] = True


def get_state(session_id: str):
    session = db.get_session(session_id)
    return {
        "score": session["score"],
        "sudden_death": session["sudden_death"],
        "game_over": session["game_over"],
    }
