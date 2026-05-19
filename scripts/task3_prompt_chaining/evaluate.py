from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from task3_prompt_chaining.executor import run_prompt_chain  # noqa: E402

QUESTIONS_CSV = ROOT / "data" / "sql_questions_only.csv"
OUTPUT_CSV = ROOT / "reports" / "task3_prompt_chain_evaluation.csv"


def main() -> None:
    OUTPUT_CSV.parent.mkdir(exist_ok=True)
    rows: list[dict[str, str]] = []

    with QUESTIONS_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for item in reader:
            question = item["question"]
            response = run_prompt_chain(question)
            rows.append({
                "Question": question,
                "Generated SQL": response.get("sql") or "",
                "Executed Successfully": "Yes" if response.get("status") == "success" else "No",
                "Correct Result": "Manual Review",
                "Retry Needed": "Yes" if response.get("retry_needed") else "No",
                "Final Status": response.get("status", "failed"),
            })

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["Question", "Generated SQL", "Executed Successfully", "Correct Result", "Retry Needed", "Final Status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    success = sum(1 for r in rows if r["Executed Successfully"] == "Yes")
    retries = sum(1 for r in rows if r["Retry Needed"] == "Yes")
    failures = total - success

    print("Question | Generated SQL | Executed Successfully | Correct Result | Retry Needed | Final Status")
    for r in rows:
        print(f"{r['Question']} | {r['Generated SQL']} | {r['Executed Successfully']} | {r['Correct Result']} | {r['Retry Needed']} | {r['Final Status']}")

    print("\nMetrics")
    print(f"SQL execution success rate: {success}/{total} = {(success / total * 100 if total else 0):.2f}%")
    print(f"Retry count: {retries}")
    print(f"Total failed queries: {failures}")
    print(f"Saved report: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
