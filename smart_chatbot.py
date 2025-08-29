import streamlit as st
import google.generativeai as genai

# Configure API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("💬 selastin Smart Chatbot ")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input box for new user message
if prompt := st.chat_input("Type your message..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Try Gemini Pro first, fallback to Flash silently
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)
    except Exception:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

    # Get reply text
    reply = response.text

    # Store assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)
