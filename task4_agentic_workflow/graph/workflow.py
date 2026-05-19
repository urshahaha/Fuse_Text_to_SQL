from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from task4_agentic_workflow.agents.executor import execute_sql
from task4_agentic_workflow.agents.planner import create_plan
from task4_agentic_workflow.agents.sql_generator import generate_sql
from task4_agentic_workflow.agents.summarizer import summarize_answer
from task4_agentic_workflow.agents.validator import validate_sql
from task4_agentic_workflow.config import MAX_AGENT_RETRIES

LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "agentic_logs.json"


@dataclass
class AgentState:
    user_query: str
    plan: dict[str, Any] | None = None
    generated_sql: str | None = None
    is_valid_sql: bool = False
    execution_results: list[dict[str, Any]] = field(default_factory=list)
    final_answer: str | None = None
    errors: list[str] = field(default_factory=list)
    attempts: int = 0
    status: str = "running"
    execution_time_ms: float = 0.0


def _write_log(state: AgentState) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if LOG_PATH.exists():
        try:
            records = json.loads(LOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            records = []
    else:
        records = []
    records.append({"timestamp": datetime.now(timezone.utc).isoformat(), **asdict(state)})
    LOG_PATH.write_text(json.dumps(records, indent=2, default=str), encoding="utf-8")


def run_agent_workflow(question: str) -> dict[str, Any]:
    started = time.perf_counter()
    state = AgentState(user_query=question)

    try:
        state.plan = create_plan(question)

        for attempt in range(1, MAX_AGENT_RETRIES + 1):
            state.attempts = attempt
            last_error = state.errors[-1] if state.errors else None
            state.generated_sql = generate_sql(question, state.plan, last_error)

            is_valid, validation_error = validate_sql(state.generated_sql)
            state.is_valid_sql = is_valid
            if not is_valid:
                state.errors.append(validation_error or "Invalid SQL")
                continue

            try:
                state.execution_results = execute_sql(state.generated_sql)
                state.final_answer = summarize_answer(question, state.generated_sql, state.execution_results)
                state.status = "success"
                break
            except Exception as exc:
                state.errors.append(str(exc))

        if state.status != "success":
            state.status = "failed"
            state.final_answer = "I could not complete the query after the allowed retry attempts."

    except Exception as exc:
        state.status = "failed"
        state.errors.append(str(exc))
        state.final_answer = "The agent could not process this request."

    state.execution_time_ms = round((time.perf_counter() - started) * 1000, 2)
    _write_log(state)
    return asdict(state)
