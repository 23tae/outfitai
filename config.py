import os
from dotenv import load_dotenv

if not load_dotenv():
    print("Warning: .env file not found")


class UtilsConfig:
    TEMP_DIRECTORY = 'tmp'
    IMG_THRESHOLD = 512


class OpenAIConfig:
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    MODEL = "gpt-4o-mini"
