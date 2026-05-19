from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from task3_prompt_chaining.executor import run_prompt_chain  # noqa: E402

st.set_page_config(page_title="Text-to-SQL Prompt Chain", page_icon="🧠", layout="wide")
st.title("Text-to-SQL Prompt Chaining Pipeline")
st.caption("Decomposition → SQL generation → validation → execution → one retry if needed")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a database question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Running prompt chain..."):
            response = run_prompt_chain(question)

        st.subheader("Generated SQL")
        st.code(response.get("sql") or "No SQL generated", language="sql")
        st.write("Status:", response.get("status"))
        st.write("Retry needed:", response.get("retry_needed"))

        result = response.get("result", [])
        if result:
            st.dataframe(pd.DataFrame(result), use_container_width=True)
        else:
            st.info("No rows returned or execution failed.")

        if response.get("error"):
            st.warning(response.get("error"))

    st.session_state.messages.append({"role": "assistant", "content": f"Status: {response.get('status')}"})
