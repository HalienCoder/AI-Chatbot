from openai import OpenAI
import streamlit as st

# — 1) Initialize Streamlit UI
st.title("AI Chatbot")

# — 2) Initialize OpenAI client from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# — 3) Persist chosen model in session_state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# — 4) Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# — 5) Render past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# — 6) Accept new user input
if prompt := st.chat_input("Say something…"):
    # 6a) Add user message to history & display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6b) Call OpenAI with streaming
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    # 6c) Save assistant reply
    st.session_state.messages.append({"role": "assistant", "content": response})
