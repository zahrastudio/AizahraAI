from api_key_manager import get_google_gemini_api_key
import requests
import time

def generate_video(prompt):
    tried_keys = set()
    max_retries = len(google_gemini_keys)
    
    while len(tried_keys) < max_retries:
        api_key = get_google_gemini_api_key()
        if api_key in tried_keys:
            continue
        tried_keys.add(api_key)

        url = "https://generativelanguage.googleapis.com/v1beta/models/veo-3.0-generate-preview:generateVideos"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key,
        }
        payload = {
            "prompt": prompt,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                print("Video berhasil digenerate!")
                return data
            else:
                print(f"Error {response.status_code} dengan API key {api_key[:8]}...: {response.text}")
        except Exception as e:
            print(f"Exception dengan API key {api_key[:8]}...: {e}")

        time.sleep(3)

    raise Exception("Gagal generate video dengan semua API key yang tersedia.")

