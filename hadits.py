import requests

def ambil_hadits():
    url = "https://api.hadith.gading.dev/hadith/random"
    try:
        res = requests.get(url).json()
        return res['data']
    except:
        return {"error": "Tidak bisa mengambil hadits"}

