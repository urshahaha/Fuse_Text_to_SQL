"""Run all 50 benchmark questions through the API pipeline.

Usage from project root after PostgreSQL is running:
    python scripts/evaluate.py

Output:
    reports/evaluation_results.csv
"""
from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.agent import run_sql_agent  # noqa: E402

QUESTIONS_CSV = ROOT / "data" / "sql_questions_only.csv"
OUTPUT_CSV = ROOT / "reports" / "evaluation_results.csv"


def main() -> None:
    OUTPUT_CSV.parent.mkdir(exist_ok=True)
    rows = []
    with QUESTIONS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for item in reader:
            question = item["question"]
            start = time.perf_counter()
            try:
                response = run_sql_agent(question)
                latency = round((time.perf_counter() - start) * 1000, 2)
                result = response.get("result")
                rows.append({
                    "question": question,
                    "generated_sql": response.get("sql"),
                    "executed_successfully": response.get("status") == "success",
                    "row_count": len(result) if isinstance(result, list) else "",
                    "retry_needed": response.get("attempts", 1) > 1,
                    "attempts": response.get("attempts"),
                    "latency_ms": latency,
                    "final_status": response.get("status"),
                    "error": response.get("error") or "",
                })
            except Exception as exc:  # noqa: BLE001
                latency = round((time.perf_counter() - start) * 1000, 2)
                rows.append({
                    "question": question,
                    "generated_sql": "",
                    "executed_successfully": False,
                    "row_count": "",
                    "retry_needed": False,
                    "attempts": 0,
                    "latency_ms": latency,
                    "final_status": "failed",
                    "error": str(exc),
                })

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved evaluation results to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
