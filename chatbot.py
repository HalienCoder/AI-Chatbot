import streamlit as st
import openai
import os

# Set your free OpenRouter API key here
openai.api_key = os.getenv("API_OPENROUTER_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

st.title("💬 Free AI Chatbot")
chat_history = st.session_state.get("history", [])

user_input = st.text_input("You:", key="user_input")
if user_input:
    chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="openchat/openchat-3.5-0106",  # free open model
            messages=chat_history
        )
    reply = response["choices"][0]["message"]["content"]
    chat_history.append({"role": "assistant", "content": reply})
    st.session_state["history"] = chat_history

for msg in chat_history:
    st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
