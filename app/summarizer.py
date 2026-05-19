from __future__ import annotations

from typing import Any


def summarize_result(question: str, result: Any, status: str) -> str:
    if status != "success":
        return "The system could not answer this question after retrying the SQL query."

    if isinstance(result, list):
        if len(result) == 0:
            return f"The query ran successfully, but no rows were returned for: {question}"
        if len(result) == 1 and len(result[0]) == 1:
            value = next(iter(result[0].values()))
            return f"The answer to '{question}' is {value}."
        return f"The query ran successfully and returned {len(result)} row(s) for: {question}"

    return f"The query ran successfully for: {question}"
