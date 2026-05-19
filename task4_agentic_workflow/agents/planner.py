from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from task4_agentic_workflow.agents.llm import call_llm, has_llm_key
from task4_agentic_workflow.prompts import PLANNER_PROMPT, SCHEMA_CONTEXT


def create_plan(question: str) -> dict[str, Any]:
    if has_llm_key():
        prompt = PLANNER_PROMPT.format(question=question, schema=SCHEMA_CONTEXT)
        return json.loads(call_llm(prompt, json_mode=True))

    from app.decomposer import decompose_question

    decomposition = decompose_question(question)
    return {
        "intent": decomposition.get("intent"),
        "tables": decomposition.get("tables"),
        "columns": decomposition.get("columns"),
        "filters": decomposition.get("filters"),
        "joins": decomposition.get("joins"),
        "strategy": "Use the benchmark mapping to generate a safe SELECT query.",
    }
