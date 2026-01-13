import streamlit as st
import google.genai as genai  # Robust import to avoid namespace issues
from google.genai import types

# 1. PAGE SETUP
st.set_page_config(page_title="Python Pete", page_icon="🐍")
st.title("🐍 Python Pete: AI Navigator")
st.markdown("---")

# 2. SECURE API KEY (Uses Streamlit Secrets)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("❌ Missing API Key! Go to Settings > Secrets and add GEMINI_API_KEY.")
    st.stop()

# 3. INITIALIZE CLIENT
client = genai.Client(api_key=api_key)

# 4. DISCOVERY ENGINE (Self-Healing)
@st.cache_resource
def get_working_model():
    try:
        # Scans your account for permitted models
        for m in client.models.list():
            if hasattr(m, 'supported_actions') and 'generateContent' in m.supported_actions:
                if "flash" in m.name.lower():
                    return m.name
        return "gemini-1.5-flash"  # Fallback
    except Exception:
        return "gemini-1.5-flash"

active_model = get_working_model()

# 5. CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. CHAT INPUT
if prompt := st.chat_input("Sss-say something to Pete..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Pete's Response
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model=active_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are Pete, a snake-like AI navigator. Use snake puns and be helpful."
                )
            )
            pete_reply = response.text
            st.markdown(pete_reply)
            st.session_state.messages.append({"role": "assistant", "content": pete_reply})
        except Exception as e:
            st.error(f"Pete had a hiccup: {e}")
