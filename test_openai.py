# import os  # FIXED: unknown import commented out
# from openai import OpenAI  # FIXED: unknown import commented out
# from dotenv import load_dotenv  # FIXED: unknown import commented out

load_dotenv()

keys = [
    os.getenv("OPENAI_API_KEY_1"),
    os.getenv("OPENAI_API_KEY_2"),
    os.getenv("OPENAI_API_KEY_3"),
]

for idx, key in enumerate(keys, start=1):
    if not key:
        print(f"API Key {idx} tidak ditemukan di environment.")
        continue

    print(f"Menguji API Key ke-{idx} ...")
    try:
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        print(f"API Key {idx} VALID! Respon: {response.choices[0].message.content.strip()}\n")
    except Exception as e:
        print(f"API Key {idx} TIDAK VALID! Error: {e}\n")