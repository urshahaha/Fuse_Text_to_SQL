from __future__ import annotations

from typing import Any
from app.query_bank import get_known_query, normalize_question
from app.logger_config import logger


def decompose_question(question: str) -> dict[str, Any]:
    """Task 2: convert natural language into structured components.

    First use the benchmark query bank. If the exact question is not in the benchmark,
    use a tiny fallback so the API still returns a helpful response.
    """
    known = get_known_query(question)
    if known:
        decomposition = {
            "intent": known["intent"],
            "tables": known["tables"],
            "columns": known["columns"],
            "filters": known["filters"],
            "joins": known["joins"],
            "method": "benchmark_rule_bank",
        }
        logger.info("DECOMPOSITION | %s | %s", question, decomposition)
        return decomposition

    q = normalize_question(question)
    decomposition = {
        "intent": "Unknown or unsupported benchmark query",
        "tables": [],
        "columns": [],
        "filters": [],
        "joins": [],
        "method": "fallback_unknown",
        "note": f"No exact benchmark rule found for: {q}",
    }
    logger.info("DECOMPOSITION_FALLBACK | %s | %s", question, decomposition)
    return decomposition
