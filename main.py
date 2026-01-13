import os
import sys
from google import genai
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: Key missing in .env")
    sys.exit()

# 2. Initialize the 2026 Client
client = genai.Client(api_key=api_key.strip())

print("🔍 Pete is scanning your specific permissions...")

# 3. THE DISCOVERY (Fixed for Library 1.57.0)
active_model = None
try:
    # We look for 'generateContent' inside the new 'supported_actions' list
    for m in client.models.list():
        if hasattr(m, 'supported_actions') and 'generateContent' in m.supported_actions:
            # We prefer 'flash' models because they are usually free
            if "flash" in m.name.lower():
                active_model = m.name
                break
    
    # If no 'flash' found, grab the first one that supports generating content
    if not active_model:
        for m in client.models.list():
            if hasattr(m, 'supported_actions') and 'generateContent' in m.supported_actions:
                active_model = m.name
                break
except Exception as e:
    print(f"❌ Scanner failed: {e}")
    sys.exit()

if not active_model:
    print("❌ No usable models found. Check your API key at aistudio.google.com")
    sys.exit()

print(f"✅ Found working model for you: {active_model}")

# 4. Start the Chat
try:
    chat = client.chats.create(model=active_model)
    print("--- Python Pete is Online! ---")
except Exception as e:
    print(f"❌ Connection error: {e}")
    sys.exit()

# 5. Simple Chat Loop
while True:
    user_msg = input("\nYou (Dona): ")
    if user_msg.lower() in ["quit", "exit", "bye"]:
        print("Pete: Sss-see you later! 🐍")
        break
    
    try:
        response = chat.send_message(user_msg)
        print(f"Pete: {response.text}")
    except Exception as e:
        print(f"❌ Pete had a hiccup: {e}")