from __future__ import annotations

from app.query_bank import get_known_query
from app.logger_config import logger


def generate_sql(question: str, decomposition: dict) -> str:
    """Task 3: convert decomposition into SQL."""
    known = get_known_query(question)
    if known:
        sql = known["sql"]
        logger.info("SQL_GENERATION | %s | %s", question, sql)
        return sql

    raise ValueError(
        "This beginner version only supports the 50 benchmark questions. "
        "Add a new rule in app/query_bank.py for this question."
    )
