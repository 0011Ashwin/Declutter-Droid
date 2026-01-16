import os
from dotenv import load_dotenv

def check_api_key():
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    print("-" * 30)
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables.")
    elif api_key == "your_api_key_here":
        print("❌ Error: GEMINI_API_KEY is still set to the default placeholder.")
    else:
        # Simple heuristic: Google API keys usually start with AIza
        if api_key.startswith("AIza"):
            print("✅ Success: GEMINI_API_KEY found and looks valid (starts with AIza).")
        else:
            print("⚠️ Warning: GEMINI_API_KEY found, but doesn't start with 'AIza'. It might be invalid.")
            print(f"Current Value: {api_key[:4]}...{api_key[-4:]}") # Obfuscated
            
    print("-" * 30)

if __name__ == "__main__":
    check_api_key()
