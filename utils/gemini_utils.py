import google.generativeai as genai
from config.config import load_config

def setup_gemini():
    config = load_config()
    genai.configure(api_key=config['api_key'])
    return genai.GenerativeModel("gemini-1.5-pro")