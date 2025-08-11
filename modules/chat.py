# import os  # FIXED: unknown import commented out
# from openai import OpenAI  # FIXED: unknown import commented out
# from dotenv import load_dotenv  # FIXED: unknown import commented out

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY tidak ditemukan di .env")

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_ai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Gagal memproses chat: {e}")
