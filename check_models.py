import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ Key not found")
else:
    genai.configure(api_key=api_key)
    print(f"🔑 Key found: {api_key[:10]}...")
    
    print("\n🔎 Listing available models for you...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ FOUND: {m.name}")
    except Exception as e:
        print(f"❌ Error: {e}")
