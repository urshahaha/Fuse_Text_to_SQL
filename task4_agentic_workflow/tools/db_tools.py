from __future__ import annotations

from typing import Any

from sqlalchemy import text

from task4_agentic_workflow.db import get_engine


def run_select_query(sql: str) -> list[dict[str, Any]]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        return [dict(row) for row in result.mappings().all()]
