import requests

def ambil_doa():
    url = "https://doa-doa-api-ahmadramadhan.fly.dev/api"
    try:
        res = requests.get(url).json()
        return res[0]  # mengambil doa pertama
    except:
        return {"error": "Gagal mengambil doa"}

