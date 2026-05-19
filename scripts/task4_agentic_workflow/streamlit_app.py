from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from task4_agentic_workflow.graph.workflow import run_agent_workflow  # noqa: E402

st.set_page_config(page_title="Agentic Text-to-SQL", page_icon="🤖", layout="wide")
st.title("Agentic Text-to-SQL Workflow")
st.caption("Planner → SQL Generator → Validator → Executor → Summarizer")

question = st.text_input("Ask a database question", value="Total number of customers")

if st.button("Run Agent") and question:
    with st.spinner("Running agent workflow..."):
        response = run_agent_workflow(question)

    st.subheader("Final Answer")
    st.write(response.get("final_answer"))

    st.subheader("Plan")
    st.json(response.get("plan"))

    st.subheader("Generated SQL")
    st.code(response.get("generated_sql") or "", language="sql")

    st.write("Status:", response.get("status"))
    st.write("Attempts:", response.get("attempts"))

    results = response.get("execution_results", [])
    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True)

    if response.get("errors"):
        st.subheader("Errors")
        st.write(response.get("errors"))
