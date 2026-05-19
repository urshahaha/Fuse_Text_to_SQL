from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from task4_agentic_workflow.config import DATABASE_URL


def get_engine() -> Engine:
    return create_engine(DATABASE_URL, pool_pre_ping=True)
