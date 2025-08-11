# api_key_manager.py
from dotenv import load_dotenv
import os
import random

load_dotenv()

# --- Ambil semua API key dari .env (sesuaikan nama variabel di .env kamu) ---
openai_keys = [os.getenv(k) for k in ["OPENAI_API_KEY_1", "OPENAI_API_KEY_2", "OPENAI_API_KEY_3", "OPENAI_API_KEY_4"]]
openai_keys = [k for k in openai_keys if k]

google_gemini_keys = [os.getenv(k) for k in ["GOOGLE_GEMINI_API_KEY_1", "GOOGLE_GEMINI_API_KEY_2"]]
google_gemini_keys = [k for k in google_gemini_keys if k]

youtube_keys = [os.getenv(k) for k in ["YOUTUBE_API_KEY_1", "YOUTUBE_API_KEY_2"]]
youtube_keys = [k for k in youtube_keys if k]

pixabay_keys = [os.getenv(k) for k in ["PIXABAY_API_KEY_1", "PIXABAY_API_KEY"]]
pixabay_keys = [k for k in pixabay_keys if k]

google_calendar_keys = [os.getenv("GOOGLE_CALENDAR_API_KEY_1")]
google_calendar_keys = [k for k in google_calendar_keys if k]

# --- index rotasi per service (round-robin) ---
current_key_indices = {
    "openai": -1,
    "google_gemini": -1,
    "youtube": -1,
    "pixabay": -1,
    "google_calendar": -1,
}

def get_key_round_robin(key_list, service_name):
    """Ambil API key berikutnya (round-robin) dari key_list."""
    if not key_list:
        raise ValueError(f"Tidak ada API key valid untuk {service_name}.")
    global current_key_indices
    current_key_indices[service_name] = (current_key_indices[service_name] + 1) % len(key_list)
    return key_list[current_key_indices[service_name]]

# fungsi-fungsi per layanan
def get_openai_api_key():
    return get_key_round_robin(openai_keys, "openai")

def get_google_gemini_api_key():
    return get_key_round_robin(google_gemini_keys, "google_gemini")

def get_youtube_api_key():
    return get_key_round_robin(youtube_keys, "youtube")

def get_pixabay_api_key():
    return get_key_round_robin(pixabay_keys, "pixabay")

def get_google_calendar_api_key():
    return get_key_round_robin(google_calendar_keys, "google_calendar")

# fungsi umum yang dipanggil oleh TUI: get_api_key("openai") dsb.
def get_api_key(service_name="openai"):
    name = service_name.lower()
    if name == "openai":
        return get_openai_api_key()
    if name in ("google_gemini", "gemini"):
        return get_google_gemini_api_key()
    if name == "youtube":
        return get_youtube_api_key()
    if name == "pixabay":
        return get_pixabay_api_key()
    if name in ("google_calendar", "calendar"):
        return get_google_calendar_api_key()
    raise ValueError(f"Service '{service_name}' tidak dikenal.")

