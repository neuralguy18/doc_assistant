import streamlit as st
import os
from dotenv import load_dotenv
from src.assistant import DocumentAssistant

api_key = os.getenv("OPENAI_API_KEY")

# Initialize assistant once
if "assistant" not in st.session_state:
    st.session_state.assistant = DocumentAssistant(
        openai_api_key= os.getenv("OPENAI_API_KEY"),
        model_name="gpt-4o",
    )
    st.session_state.session_id = st.session_state.assistant.start_session(user_id="user123")

# Prepare chat history in UI
if "message_history" not in st.session_state:
    st.session_state.message_history = []

st.title("Document Assistant")

# Display previous messages
for msg in st.session_state.message_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type here")

if user_input:
    # Show user message
    st.session_state.message_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Process message with DocumentAssistant
    result = st.session_state.assistant.process_message(user_input)

    ai_response = result.get("response", "[No response]")

    # Show assistant reply
    st.session_state.message_history.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.write(ai_response)
