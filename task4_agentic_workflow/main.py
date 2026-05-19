from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from task4_agentic_workflow.graph.workflow import run_agent_workflow

app = FastAPI(title="Agentic Text-to-SQL Workflow")


class QuestionRequest(BaseModel):
    question: str


@app.post("/agent/sql")
def agent_sql(payload: QuestionRequest) -> dict:
    return run_agent_workflow(payload.question)
