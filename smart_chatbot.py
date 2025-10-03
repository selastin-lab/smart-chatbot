import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import asyncio
import edge_tts
import os
import tempfile
import time
from langdetect import detect

# -------------------------
# Configure Gemini API
# -------------------------
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyAZigZw2dkBTq5MsXJ4k95dsDMzijRmym8")
if not GEMINI_KEY:
    st.error("⚠️ Gemini API key not found. Please add it to .streamlit/secrets.toml")
genai.configure(api_key=GEMINI_KEY)

st.set_page_config(page_title="Milini Chatbot", page_icon="🤖", layout="wide")
st.title("💬 Milini Chatbot")

# -------------------------
# Session state initialization
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# -------------------------
# Generate response using Gemini
# -------------------------
def generate_response(prompt: str) -> str:
    if not prompt.strip():
        return "I didn't hear anything — please try again."
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")  # valid Gemini model
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini error: {e}"

# -------------------------
# Decide whether to speak
# -------------------------
def should_speak(reply: str) -> bool:
    if not reply or "```" in reply or len(reply) > 500:
        return False
    lower = reply.lower()
    if ("http" in lower or "dataset" in lower or "model" in lower) and len(reply) > 200:
        return False
    return True

# -------------------------
# TTS using edge-tts
# -------------------------
async def _speak_async(text: str, voice: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tmp_path = f.name
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(tmp_path)

    # Play audio
    if os.name == "posix":
        for cmd in (f"afplay {tmp_path}", f"mpv --no-video --really-quiet {tmp_path}", f"mpg123 {tmp_path}"):
            if os.system(cmd + " >/dev/null 2>&1") == 0:
                break
        else:
            st.audio(tmp_path, format="audio/mp3")
    else:
        os.startfile(tmp_path)

    time.sleep(0.2)
    try:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    except Exception:
        pass

def speak_text(reply: str, lang: str = "en"):
    if not reply:
        return
    voice = "en-US-JennyNeural" if lang == "en" else "ta-IN-PallaviNeural"
    try:
        asyncio.run(_speak_async(reply, voice))
    except Exception:
        st.warning("TTS failed — showing audio widget instead.")

# -------------------------
# Speech recognition
# -------------------------
recognizer = sr.Recognizer()

def listen_to_user(timeout=5, phrase_time_limit=8):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        st.info("🎤 Listening... speak now")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            st.info("No speech detected (timed out).")
            return "", None

    try:
        try:
            text = recognizer.recognize_google(audio, language="ta-IN")
            return text, "ta"
        except sr.UnknownValueError:
            text = recognizer.recognize_google(audio, language="en-US")
            return text, "en"
    except sr.UnknownValueError:
        st.info("Sorry — couldn't understand. Please try again.")
        return "", None
    except sr.RequestError:
        st.error("Speech recognition service error.")
        return "", None

# -------------------------
# Language detection
# -------------------------
def detect_lang_safe(text: str) -> str:
    try:
        return "ta" if detect(text) == "ta" else "en"
    except Exception:
        return "en"

# -------------------------
# Display chat history
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# -------------------------
# First-time greeting
# -------------------------
if not st.session_state.greeted:
    greeting = "Hi — I'm Milini, your humanoid robot assistant. How can I help you today?"
    st.session_state.messages.append({"role":"assistant","content":greeting})
    st.chat_message("assistant").markdown(greeting)
    speak_text(greeting, lang="en")
    st.session_state.greeted = True

# -------------------------
# Bottom input row
# -------------------------
input_col, mic_col = st.columns([6, 1])
with input_col:
    typed = st.chat_input("Type your message...")
with mic_col:
    mic_clicked = st.button("🎤")

# -------------------------
# Handle mic input
# -------------------------
user_text = ""
lang = None
if mic_clicked:
    user_text, lang = listen_to_user()
    if user_text:
        st.session_state.messages.append({"role":"user","content":user_text})
        st.chat_message("user").markdown(user_text)

# -------------------------
# Handle typed input
# -------------------------
if typed:
    user_text = typed
    lang = detect_lang_safe(user_text)
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.chat_message("user").markdown(user_text)

# -------------------------
# Generate and show reply
# -------------------------
if user_text:
    reply = generate_response(user_text)
    st.session_state.messages.append({"role":"assistant","content":reply})
    st.chat_message("assistant").markdown(reply)

    if should_speak(reply):
        if not lang:
            lang = detect_lang_safe(reply or user_text)
        speak_text(reply, lang=lang)
    else:
        st.info("Response shown (voice suppressed for code/long text).")
