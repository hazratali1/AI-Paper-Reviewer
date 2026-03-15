import os
from groq import Groq
from dotenv import load_dotenv

# Use absolute path to .env
env_path = os.path.join(os.getcwd(), 'backend', '.env')
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    print("Error: No GROQ_API_KEY found in .env")
else:
    print(f"Testing Groq API Key: {api_key[:10]}...")
    try:
        client = Groq(api_key=api_key)
        # Try a tiny request
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print("Success: API Key is working!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Error testing Groq API: {e}")
        # Try a different model just in case
        try:
            print("Trying llama-3.1-8b-instant...")
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=5
            )
            print("Success with fallback model!")
        except Exception as e2:
            print(f"Fallback also failed: {e2}")
