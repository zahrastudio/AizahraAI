import requests

def ambil_doa():
    try:
        url = "https://doa-doa-api-ahmadramadhan.fly.dev/api"
        res = requests.get(url).json()
        return res[0]
    except Exception:
        return {"error": "Doa API bermasalah"}

def ambil_doa():
    try:
        return {
            "doa": "Doa sebelum tidur",
            "arab": "بِاسْمِكَ اللّهُمَّ أَحْيَا وَأَمُوتُ",
            "arti": "Dengan nama-Mu ya Allah, aku hidup dan aku mati"
        }
    except Exception as e:
        return {"error": str(e)}

