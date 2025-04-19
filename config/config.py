import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    return {
        'api_key': os.getenv('GEMINI_API_KEY')
    }