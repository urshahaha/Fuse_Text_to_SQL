from __future__ import annotations

from typing import Any

from task4_agentic_workflow.tools.db_tools import run_select_query


def execute_sql(sql: str) -> list[dict[str, Any]]:
    return run_select_query(sql)
