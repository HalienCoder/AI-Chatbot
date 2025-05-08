import streamlit as st
import os
from openai import OpenAI

# Setup client with OpenRouter API base and key
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

st.title("AI Chatbot")
st.markdown("Developed by Nihal and Magin")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:", key="user_input")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="openchat/openchat-3.5-0106",
            messages=st.session_state.history
        )
        reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": reply})

# Display chat
for msg in st.session_state.history:
    st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
