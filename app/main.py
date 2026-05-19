from __future__ import annotations

from fastapi import FastAPI
from app.agent import run_sql_agent, run_text_to_sql_pipeline
from app.decomposer import decompose_question
from app.models import QuestionRequest, QueryResponse

app = FastAPI(
    title="Week 3 Agentic Text-to-SQL System",
    description="FastAPI + PostgreSQL project for Tasks 2, 3 and 4.",
    version="1.0.0",
)


@app.get("/")
def home() -> dict:
    return {
        "message": "Text-to-SQL API is running.",
        "try_docs": "Open http://localhost:8000/docs",
        "task2": "POST /decompose",
        "task3": "POST /text-to-sql",
        "task4": "POST /agent/sql",
    }


@app.post("/decompose")
def decompose(payload: QuestionRequest) -> dict:
    return {"question": payload.question, "decomposition": decompose_question(payload.question)}


@app.post("/text-to-sql", response_model=QueryResponse)
def text_to_sql(payload: QuestionRequest) -> dict:
    # Task 3 says maximum retry limit is 1 retry.
    return run_text_to_sql_pipeline(payload.question, max_retries=1)


@app.post("/agent/sql", response_model=QueryResponse)
def agent_sql(payload: QuestionRequest) -> dict:
    # Task 4 says retry up to 3 times maximum.
    return run_sql_agent(payload.question)
