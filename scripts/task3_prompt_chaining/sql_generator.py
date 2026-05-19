from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from task3_prompt_chaining.prompts.templates import (
    DECOMPOSITION_PROMPT,
    SCHEMA_CONTEXT,
    SQL_FIX_PROMPT,
    SQL_GENERATION_PROMPT,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")


def _has_openai_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def _call_openai(prompt: str, *, json_mode: bool = False) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    kwargs: dict[str, Any] = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()


def _clean_sql(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```sql", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"^```", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    return text.rstrip(";")


def _fallback_decompose(question: str) -> dict[str, Any]:
    from app.decomposer import decompose_question

    return decompose_question(question)


def _fallback_generate(question: str, decomposition: dict[str, Any]) -> str:
    from app.sql_generator import generate_sql

    return generate_sql(question, decomposition)


def _fallback_fix(sql: str, error: str) -> str:
    from app.self_correction import try_fix_sql

    return try_fix_sql(sql, error)


def decompose_question_llm(question: str) -> dict[str, Any]:
    if not _has_openai_key():
        return _fallback_decompose(question)

    prompt = DECOMPOSITION_PROMPT.format(question=question, schema=SCHEMA_CONTEXT)
    raw = _call_openai(prompt, json_mode=True)
    return json.loads(raw)


def generate_sql_llm(question: str, decomposition: dict[str, Any]) -> str:
    if not _has_openai_key():
        return _fallback_generate(question, decomposition)

    prompt = SQL_GENERATION_PROMPT.format(
        decomposition=json.dumps(decomposition, indent=2),
        schema=SCHEMA_CONTEXT,
    )
    return _clean_sql(_call_openai(prompt))


def fix_sql_llm(question: str, sql: str, error: str) -> str:
    if not _has_openai_key():
        return _fallback_fix(sql, error)

    prompt = SQL_FIX_PROMPT.format(
        question=question,
        sql=sql,
        error=error,
        schema=SCHEMA_CONTEXT,
    )
    return _clean_sql(_call_openai(prompt))
