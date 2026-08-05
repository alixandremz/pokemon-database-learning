import re

BLOCKED_KEYWORDS = [
    "drop", "delete", "update", "insert", "alter", "attach", "detach",
    "pragma", "vacuum", "replace", "create", "trigger", "sqlite_master",
]


def validate_select(sql: str) -> str:
    """Valida que o SQL é um único comando SELECT seguro.
    Retorna o SQL limpo ou lança ValueError com o motivo da rejeição."""
    cleaned = sql.strip()
    if not cleaned:
        raise ValueError("a query está vazia")

    if cleaned.endswith(";"):
        cleaned = cleaned[:-1]
    if ";" in cleaned:
        raise ValueError("só é permitido 1 comando por vez")

    if not re.match(r"^\s*select\b", cleaned, re.IGNORECASE):
        raise ValueError("só comandos SELECT são permitidos")

    lowered = cleaned.lower()
    for word in BLOCKED_KEYWORDS:
        if re.search(rf"\b{word}\b", lowered):
            raise ValueError(f"palavra bloqueada na query: {word}")

    return cleaned
