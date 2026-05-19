from __future__ import annotations

from app.decomposer import decompose_question
from app.executor import execute_with_retry
from app.sql_generator import generate_sql
from app.summarizer import summarize_result
from app.logger_config import logger


def run_text_to_sql_pipeline(question: str, max_retries: int = 1) -> dict:
    """Task 3 pipeline: decompose -> SQL -> execute -> one retry."""
    decomposition = decompose_question(question)
    sql = generate_sql(question, decomposition)
    result, final_sql, status, attempts, execution_time_ms, error = execute_with_retry(sql, max_retries=max_retries)
    summary = summarize_result(question, result, status)
    logger.info("PIPELINE_OUTPUT | status=%s | attempts=%s | question=%s", status, attempts, question)
    return {
        "question": question,
        "decomposition": decomposition,
        "sql": final_sql,
        "result": result,
        "summary": summary,
        "status": status,
        "attempts": attempts,
        "execution_time_ms": round(execution_time_ms, 2),
        "error": error,
    }


def run_sql_agent(question: str) -> dict:
    """Task 4 agent: same flow but allows up to 3 retries."""
    return run_text_to_sql_pipeline(question, max_retries=3)
