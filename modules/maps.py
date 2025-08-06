import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

def cari_gambar_pixabay(keyword, jumlah=3):
    if not PIXABAY_API_KEY:
        return []

    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={quote_plus(keyword)}&image_type=photo&per_page={jumlah}"
    try:
        res = requests.get(url)
        data = res.json()
        return data.get("hits", [])[:jumlah]
    except Exception as e:
        print("❌ Error saat mengambil gambar:", e)
        return []

def link_google_maps(keyword):
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(keyword)}"
