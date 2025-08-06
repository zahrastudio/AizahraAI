import os
from dotenv import load_dotenv

# Muat variabel dari file .env
load_dotenv("env")

# Ambil API Key dari environment
google_key1 = os.getenv("GOOGLE_API_KEY1")
google_key2 = os.getenv("GOOGLE_API_KEY2")
pixabay_key = os.getenv("PIXABAY_API_KEY")
mapillary_token = os.getenv("MAPILLARY_TOKEN")

print("🔐 API Keys Loaded:")
print("Google Key 1:", google_key1)
print("Google Key 2:", google_key2)
print("Pixabay Key :", pixabay_key)
print("Mapillary Token:", mapillary_token)

