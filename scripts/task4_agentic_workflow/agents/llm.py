from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from task4_agentic_workflow.config import OPENAI_MODEL


def has_llm_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def call_llm(prompt: str, *, json_mode: bool = False) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    kwargs: dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()
