from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from task3_prompt_chaining.database import execute_select
from task3_prompt_chaining.sql_generator import (
    decompose_question_llm,
    fix_sql_llm,
    generate_sql_llm,
)
from task3_prompt_chaining.validator import validate_select_only

LOG_PATH = Path(__file__).resolve().parent / "logs" / "query_logs.json"


def _append_log(record: dict[str, Any]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LOG_PATH.exists():
        try:
            logs = json.loads(LOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            logs = []
    else:
        logs = []
    logs.append(record)
    LOG_PATH.write_text(json.dumps(logs, indent=2, default=str), encoding="utf-8")


def run_prompt_chain(question: str) -> dict[str, Any]:
    start = time.perf_counter()
    retry_needed = False
    error_message: str | None = None

    try:
        decomposition = decompose_question_llm(question)
        sql = generate_sql_llm(question, decomposition)

        is_valid, validation_error = validate_select_only(sql)
        if not is_valid:
            raise ValueError(validation_error)

        try:
            result = execute_select(sql)
            status = "success"
        except Exception as exc:
            retry_needed = True
            error_message = str(exc)
            fixed_sql = fix_sql_llm(question, sql, error_message)
            is_valid, validation_error = validate_select_only(fixed_sql)
            if not is_valid:
                raise ValueError(validation_error)
            result = execute_select(fixed_sql)
            sql = fixed_sql
            status = "success"

        response = {
            "question": question,
            "decomposition": decomposition,
            "sql": sql,
            "result": result,
            "status": status,
            "retry_needed": retry_needed,
            "error": error_message,
            "execution_time_ms": round((time.perf_counter() - start) * 1000, 2),
        }
    except Exception as exc:
        response = {
            "question": question,
            "sql": None,
            "result": [],
            "status": "failed",
            "retry_needed": retry_needed,
            "error": str(exc),
            "execution_time_ms": round((time.perf_counter() - start) * 1000, 2),
        }

    _append_log({"timestamp": datetime.now(timezone.utc).isoformat(), **response})
    return response
