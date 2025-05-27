import os
import streamlit as st
import requests

# Read API_URL from env
API_URL = os.getenv("API_URL")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

# Title and caption
st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("Talk to your AI Assistant!")
st.caption("Powered by o4-mini")
st.info(f"📡 Sending requests to: {API_URL}")

# Chat input form
with st.form("chat_form", clear_on_submit=True):
    query = st.text_input("Ask a question:")
    send = st.form_submit_button("Send")

    if send and query:
        # 1) Append user message
        st.session_state.messages.append({"role": "user", "content": query})

        # 2) Call backend
        try:
            r = requests.post(API_URL, json={"messages": st.session_state.messages})
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"Error calling {API_URL}: {e}")
            if "r" in locals():
                st.text(f"Status {r.status_code}\n{r.text}")
            st.stop()

        # 3) Append assistant response and store sources
        st.session_state.messages.append({"role": "assistant", "content": data["response"]})
        st.session_state.last_sources = data.get("sources", [])

# 4) Render full conversation
for msg in st.session_state.messages:
    speaker = "You" if msg["role"] == "user" else "AI Assistant"
    st.markdown(f"**{speaker}:** {msg['content']}")

# 5) Show sources from last submission
if st.session_state.last_sources:
    with st.expander("Sources Used"):
        for src in st.session_state.last_sources:
            st.write(f"- {src['doc_id']} (chunk {src['chunk_id']})")
