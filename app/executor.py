from __future__ import annotations

import time
from app.database import run_sql
from app.logger_config import logger
from app.self_correction import try_fix_sql
from app.validator import validate_select_only


def execute_with_retry(sql: str, max_retries: int = 1) -> tuple[list[dict] | None, str, str, int, float, str | None]:
    """Execute SQL safely with retry.

    Returns: result, final_sql, status, attempts, execution_time_ms, error
    """
    current_sql = sql
    start = time.perf_counter()
    last_error = None

    for attempt in range(1, max_retries + 2):
        try:
            validate_select_only(current_sql)
            query_start = time.perf_counter()
            result = run_sql(current_sql)
            elapsed_ms = (time.perf_counter() - query_start) * 1000
            logger.info("SQL_EXECUTION_SUCCESS | attempt=%s | %.2fms | %s", attempt, elapsed_ms, current_sql)
            total_ms = (time.perf_counter() - start) * 1000
            return result, current_sql, "success", attempt, total_ms, None
        except Exception as exc:  # noqa: BLE001 - we need DB error text for self-correction
            last_error = str(exc)
            logger.error("SQL_EXECUTION_ERROR | attempt=%s | error=%s | sql=%s", attempt, last_error, current_sql)
            if attempt > max_retries:
                break
            current_sql = try_fix_sql(current_sql, last_error)
            logger.info("SQL_RETRY_GENERATED | next_attempt=%s | %s", attempt + 1, current_sql)

    total_ms = (time.perf_counter() - start) * 1000
    return None, current_sql, "failed", max_retries + 1, total_ms, last_error
