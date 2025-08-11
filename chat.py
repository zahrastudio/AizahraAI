
# modules/chat.py

import os
import openai
from dotenv import load_dotenv

# Muat file .env untuk kunci API
load_dotenv()

# Ambil kunci OpenAI dari environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Fungsi utama untuk mengirim prompt ke OpenAI Chat API
def tanya_ai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Kamu adalah asisten Islami yang membantu menjawab dengan bijak, akurat, dan sopan."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Terjadi kesalahan saat menghubungi AI: {str(e)}"

