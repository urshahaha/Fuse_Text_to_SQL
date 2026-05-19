"""Small helper to verify that the seed database loaded correctly."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database import run_sql  # noqa: E402

TABLES = ["productlines", "products", "offices", "employees", "customers", "payments", "orders", "orderdetails"]

for table in TABLES:
    rows = run_sql(f'SELECT COUNT(*) AS count FROM {table};')
    print(f"{table}: {rows[0]['count']}")
