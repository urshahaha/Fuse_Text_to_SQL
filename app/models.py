from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(..., examples=["How many shipped orders are from USA customers?"])


class QueryResponse(BaseModel):
    question: str
    decomposition: dict[str, Any]
    sql: str
    result: Any
    summary: str
    status: str
    attempts: int = 1
    execution_time_ms: Optional[float] = None
    error: Optional[str] = None
