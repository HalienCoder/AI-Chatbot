import os
import time
import streamlit as st
from openai import OpenAI, error  # error contains RateLimitError

# Initialize client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

st.title("AI Chatbot")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input box
user_input = st.text_input("You:", key="user_input")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.user_input = ""  # clear input

    # Retry parameters
    max_retries = 5
    backoff_base = 1  # start with 1 second

    with st.spinner("Thinking..."):
        for attempt in range(1, max_retries + 1):
            try:
                # Streaming call
                stream = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo:free",
                    messages=st.session_state.history,
                    stream=True,
                )
                # Collect the response token-by-token
                full_reply = ""
                for token in stream:
                    delta = token.choices[0].delta.get("content", "")
                    full_reply += delta
                    st.write(delta, end="")  # typewriter effect

                # Save in history and break out
                st.session_state.history.append({"role": "assistant", "content": full_reply})
                break

            except error.RateLimitError as e:
                wait = backoff_base * (2 ** (attempt - 1))
                st.warning(f"Rate limit hit. Retrying in {wait} s... (Attempt {attempt}/{max_retries})")
                time.sleep(wait)
        else:
            # All retries failed
            st.error("Sorry, we’re being rate-limited. Please try again later.")
