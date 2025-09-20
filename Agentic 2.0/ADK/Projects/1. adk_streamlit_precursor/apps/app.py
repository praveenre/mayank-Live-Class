"""
Streamlit 'hello world' for ADK API + Tavily MCP.

- Sidebar: create/reset session (POST /apps/{app}/users/{user}/sessions/{session})
- Main: ask a question (POST /run) → show final answer
- Also shows "search text" parsed from tool/function call arguments (best effort)
"""

import os
import uuid
import json
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ---- Config (editable in sidebar) ----
DEFAULT_API_BASE = os.getenv("ADK_API_BASE", "http://localhost:8000")
DEFAULT_APP      = os.getenv("ADK_APP_SIMPLE", "simple")
DEFAULT_USER     = os.getenv("ADK_USER_ID", f"user-{uuid.uuid4()}")

st.set_page_config(page_title="ADK + Streamlit: Simple Q&A", layout="centered")
st.title("🔍 ADK API + Streamlit — Simple Q&A (shows search text)")
st.caption("Front end: Streamlit • Backend: ADK API Server • Tooling: Tavily MCP (search when needed)")

# ---- Session state ----
if "api_base" not in st.session_state:
    st.session_state.api_base = DEFAULT_API_BASE
if "app_name" not in st.session_state:
    st.session_state.app_name = DEFAULT_APP
if "user_id" not in st.session_state:
    st.session_state.user_id = DEFAULT_USER
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "last_response" not in st.session_state:
    st.session_state.last_response = None

# ---- Helpers ----
def create_session():
    """Call: POST /apps/{app}/users/{user}/sessions/{session}"""
    sid = f"session-{uuid.uuid4()}"
    url = f"{st.session_state.api_base}/apps/{st.session_state.app_name}/users/{st.session_state.user_id}/sessions/{sid}"
    r = requests.post(url, headers={"Content-Type":"application/json"}, json={})
    r.raise_for_status()
    st.session_state.session_id = sid
    return sid

def run_turn(question: str) -> dict:
    """Call: POST /run"""
    url = f"{st.session_state.api_base}/run"
    payload = {
        "app_name": st.session_state.app_name,
        "user_id": st.session_state.user_id,
        "session_id": st.session_state.session_id,
        "new_message": {"role":"user","parts":[{"text": question}]},
    }
    r = requests.post(url, headers={"Content-Type":"application/json"}, json=payload)
    r.raise_for_status()
    return r.json()

def parse_final_text(resp: dict) -> str:
    """Best-effort: last text part in events."""
    events = resp.get("events", resp if isinstance(resp, list) else [resp])
    final_text = ""
    for ev in events:
        content = ev.get("content", {})
        parts = content.get("parts", []) if isinstance(content, dict) else []
        for p in parts:
            if isinstance(p, dict) and isinstance(p.get("text"), str):
                txt = p["text"].strip()
                if txt:
                    final_text = txt
    return final_text

def parse_search_queries(resp: dict) -> list[str]:
    """Collect common 'query' fields from function/tool call shapes."""
    queries = []
    def walk(o):
        if isinstance(o, dict):
            # functionCall.args.query
            fc = o.get("functionCall")
            if isinstance(fc, dict):
                q = (fc.get("args") or {}).get("query")
                if isinstance(q, str) and q.strip():
                    queries.append(q.strip())
            # function_call.arguments.query
            fc2 = o.get("function_call")
            if isinstance(fc2, dict):
                q2 = (fc2.get("arguments") or {}).get("query")
                if isinstance(q2, str) and q2.strip():
                    queries.append(q2.strip())
            # tool_request.arguments.query
            tr = o.get("tool_request")
            if isinstance(tr, dict):
                q3 = (tr.get("arguments") or {}).get("query")
                if isinstance(q3, str) and q3.strip():
                    queries.append(q3.strip())
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for it in o:
                walk(it)
    walk(resp)
    # de-dup preserve order
    seen, out = set(), []
    for q in queries:
        if q not in seen:
            seen.add(q); out.append(q)
    return out

# ---- Sidebar ----
with st.sidebar:
    st.subheader("Server & Session")
    st.text_input("ADK API Base", value=st.session_state.api_base, key="api_base")
    st.text_input("App Name", value=st.session_state.app_name, key="app_name")
    st.text_input("User ID", value=st.session_state.user_id, key="user_id")

    if st.button("Create / Reset Session", use_container_width=True):
        sid = create_session()
        st.success(f"Session created: {sid}")

    if st.session_state.session_id:
        st.info(f"Active session: {st.session_state.session_id}")
    else:
        st.warning("Create a session to begin.")

st.divider()

# ---- Main ----
st.subheader("Ask a question")
question = st.text_input("Your question", "What is retrieval augmented generation?")
col1, col2 = st.columns([1,1])
with col1:
    ask_clicked = st.button("Ask", use_container_width=True)
with col2:
    show_raw = st.checkbox("Show raw events", value=False)

if st.session_state.session_id and ask_clicked:
    resp = run_turn(question)
    st.session_state.last_response = resp

    # Final answer
    answer = parse_final_text(resp)
    st.success("Answer:")
    st.write(answer or "_(No final text found)_")

    # Search text (queries) used by tools
    st.subheader("Search text (from tool calls)")
    for q in parse_search_queries(resp):
        st.code(q, language="text")

# Optional: show raw response for learning
if st.session_state.last_response and show_raw:
    st.subheader("Raw events (from /run)")
    st.code(json.dumps(st.session_state.last_response, indent=2), language="json")
