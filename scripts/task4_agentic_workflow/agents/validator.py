from __future__ import annotations

import re

BLOCKED = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE"]


def validate_sql(sql: str) -> tuple[bool, str | None]:
    sql_clean = sql.strip().rstrip(";")
    if not re.match(r"^SELECT\b", sql_clean, flags=re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    upper_sql = sql_clean.upper()
    for word in BLOCKED:
        if re.search(rf"\b{word}\b", upper_sql):
            return False, f"Blocked unsafe keyword: {word}"

    if ";" in sql_clean:
        return False, "Multiple statements are not allowed."

    return True, None
