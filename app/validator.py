from __future__ import annotations

import re

DANGEROUS_WORDS = {
    "insert", "update", "delete", "drop", "alter", "truncate", "create",
    "grant", "revoke", "merge", "call", "copy", "execute", "do"
}


def validate_select_only(sql: str) -> None:
    """Block anything that is not a single read-only SELECT query."""
    cleaned = sql.strip()
    lowered = cleaned.lower()

    if not lowered.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    # Remove one final semicolon, then disallow extra semicolons.
    no_final_semicolon = cleaned[:-1] if cleaned.endswith(";") else cleaned
    if ";" in no_final_semicolon:
        raise ValueError("Multiple SQL statements are not allowed.")

    tokens = set(re.findall(r"\b[a-zA-Z_]+\b", lowered))
    blocked = sorted(tokens.intersection(DANGEROUS_WORDS))
    if blocked:
        raise ValueError(f"Unsafe SQL keyword detected: {blocked}")

    if "--" in cleaned or "/*" in cleaned or "*/" in cleaned:
        raise ValueError("SQL comments are not allowed in generated queries.")
