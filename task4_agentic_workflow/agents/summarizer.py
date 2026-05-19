from __future__ import annotations

import json
from typing import Any

from task4_agentic_workflow.agents.llm import call_llm, has_llm_key
from task4_agentic_workflow.prompts import SUMMARY_PROMPT


def summarize_answer(question: str, sql: str, result: list[dict[str, Any]]) -> str:
    if has_llm_key():
        prompt = SUMMARY_PROMPT.format(
            question=question,
            sql=sql,
            result=json.dumps(result[:20], default=str),
        )
        return call_llm(prompt)

    if not result:
        return "The query executed successfully but returned no rows."

    if len(result) == 1 and len(result[0]) == 1:
        value = next(iter(result[0].values()))
        return f"The answer is {value}."

    return f"The query returned {len(result)} row(s)."
