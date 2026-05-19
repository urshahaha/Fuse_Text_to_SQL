from __future__ import annotations

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/textsql",
)

engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def run_sql(sql: str) -> list[dict]:
    """Execute a safe SELECT query and return rows as dictionaries."""
    with engine.connect() as connection:
        result = connection.execute(text(sql))
        rows = result.mappings().all()
        return [dict(row) for row in rows]
