from __future__ import annotations

import re

BLOCKED_KEYWORDS = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE"]


def validate_select_only(sql: str) -> tuple[bool, str | None]:
    cleaned = sql.strip().rstrip(";")
    if not cleaned:
        return False, "SQL query is empty."

    if not re.match(r"^SELECT\b", cleaned, flags=re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    upper_sql = cleaned.upper()
    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            return False, f"Unsafe keyword blocked: {keyword}"

    # Block multiple statements.
    if ";" in cleaned:
        return False, "Multiple SQL statements are not allowed."

    return True, None
