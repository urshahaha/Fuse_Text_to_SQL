from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5433/textsql"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


def execute_select(sql: str) -> list[dict[str, Any]]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.mappings().all()
        return [dict(row) for row in rows]
