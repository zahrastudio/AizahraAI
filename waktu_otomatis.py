import requests
from datetime import datetime

API_KEY = "YIJSV0BFBF8D"

def get_timezone_by_ip():
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=ip"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        zona = data['zoneName']
        waktu_lokal = data['formatted']
        gmt_offset = data['gmtOffset'] // 3600
        return {
            "zona": zona,
            "waktu_lokal": waktu_lokal,
            "utc_offset": gmt_offset
        }
    else:
        raise Exception("Gagal mengambil data zona waktu")

# Jalankan fungsi
try:
    info = get_timezone_by_ip()
    print("📍 Zona Waktu Saat Ini:", info["zona"])
    print("🕒 Waktu Lokal:", info["waktu_lokal"])
    print("🕘 UTC Offset:", f"UTC{'+' if info['utc_offset'] >=0 else ''}{info['utc_offset']}")
except Exception as e:
    print("❌ Gagal:", e)

