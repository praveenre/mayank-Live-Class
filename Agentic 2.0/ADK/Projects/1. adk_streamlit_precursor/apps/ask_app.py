import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from common.adk_client import ADKClient

load_dotenv()

API_BASE = os.getenv("ADK_API_BASE", "http://localhost:8000")
APP_SIMPLE = os.getenv("ADK_APP_SIMPLE", "simple")
DEFAULT_USER = os.getenv("ADK_USER_ID", f"user-{uuid.uuid4()}")

st.set_page_config(page_title="ADK + Streamlit: Simple Q&A", layout="centered")

st.title("💡 ADK API + Streamlit — Simple Q&A")
st.caption("Front end: Streamlit • Backend: ADK API Server • Tools: Tavily MCP (search when needed)")

if "user_id" not in st.session_state:
    st.session_state.user_id = DEFAULT_USER
if "session_id" not in st.session_state:
    st.session_state.session_id = None

client = ADKClient(API_BASE)

with st.sidebar:
    st.subheader("Server & Session")
    st.text_input("ADK API Base", value=API_BASE, key="api_base")
    st.text_input("App Name", value=APP_SIMPLE, key="app_name")
    st.text_input("User ID", value=st.session_state.user_id, key="user_id")
    if st.button("Create / Reset Session", use_container_width=True):
        sid = client.create_session(st.session_state.app_name, st.session_state.user_id)
        st.session_state.session_id = sid
        st.success(f"Session created: {sid}")

    if st.session_state.session_id:
        st.info(f"Active session: {st.session_state.session_id}")
    else:
        st.warning("Create a session to begin.")

st.divider()

st.subheader("Ask a question")
prompt = st.text_input("Your question", "What is retrieval augmented generation?")
st.write("Tip: Ask factual questions; the agent will search the web via Tavily MCP when needed.")

if st.session_state.session_id and st.button("Ask", use_container_width=True):
    resp = client.run(st.session_state.app_name, st.session_state.user_id, st.session_state.session_id, prompt)
    final_text = client.parse_events_for_text(resp)
    if final_text:
        st.success("Answer:")
        st.write(final_text)
    else:
        st.info("No final text found in response. Check your API server logs.")

st.caption("This is the minimal ‘hello world’ for Streamlit + ADK API: create a session, send a message, render the agent’s answer.")
