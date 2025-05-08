import os
import streamlit as st
from openai import OpenAI

# 1️⃣ Make sure your Streamlit secret is set as OPENAI_API_KEY (not OPENROUTER_API_KEY)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

st.title("💬 Free AI Chatbot")
st.markdown("Powered by GPT-3.5 Turbo Free (via OpenRouter)")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", key="user_input")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo:free",           # ← Valid, free-tier chat model
            messages=st.session_state.history
        )
        reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": reply})

for msg in st.session_state.history:
    st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
