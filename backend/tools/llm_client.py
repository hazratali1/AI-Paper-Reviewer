import os
from groq import Groq
from dotenv import load_dotenv

def get_groq_client():
    """
    Returns a Groq client initialized with the latest key from .env.
    By calling load_dotenv(override=True) here, we ensure that if 
    the .env file changes, the next call will use the new key.
    """
    # Force reload environment variables from .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(env_path, override=True)
    
    api_key = os.environ.get("GROQ_API_KEY", "")
    return Groq(api_key=api_key)
