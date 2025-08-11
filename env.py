from dotenv import load_dotenv
import os

load_dotenv()  # akan membaca file .env di folder saat ini

def print_env_vars():
    print("OPENAI_API_KEY_1:", os.getenv("OPENAI_API_KEY_1"))
    print("GOOGLE_GEMINI_API_KEY_1:", os.getenv("GOOGLE_GEMINI_API_KEY_1"))
    print("YOUTUBE_API_KEY_1:", os.getenv("YOUTUBE_API_KEY_1"))
    print("PIXABAY_API_KEY_1:", os.getenv("PIXABAY_API_KEY_1"))
    print("TELEGRAM_BOT_TOKEN:", os.getenv("TELEGRAM_BOT_TOKEN"))

if __name__ == "__main__":
    print_env_vars()

