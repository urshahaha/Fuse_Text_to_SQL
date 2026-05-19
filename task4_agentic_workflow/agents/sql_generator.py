from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from task4_agentic_workflow.agents.llm import call_llm, has_llm_key
from task4_agentic_workflow.prompts import SCHEMA_CONTEXT, SQL_GENERATOR_PROMPT


def _clean_sql(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```sql", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return text.rstrip(";")


def generate_sql(question: str, plan: dict[str, Any], error: str | None = None) -> str:
    if has_llm_key():
        prompt = SQL_GENERATOR_PROMPT.format(
            plan=json.dumps(plan, indent=2),
            schema=SCHEMA_CONTEXT,
            error=error or "None",
        )
        return _clean_sql(call_llm(prompt))

    from app.decomposer import decompose_question
    from app.sql_generator import generate_sql as generate_rule_sql

    return generate_rule_sql(question, decompose_question(question))
