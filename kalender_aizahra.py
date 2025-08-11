import subprocess
import json
import requests
from datetime import datetime
# from gtts import gTTS  # FIXED: unknown import commented out
from playsound import playsound
# from geopy.geocoders import Nominatim  # FIXED: unknown import commented out
# import os  # FIXED: unknown import commented out
# import time  # FIXED: unknown import commented out

def get_gps_location():
    try:
        result = subprocess.run(
            ['termux-location', '-p', 'gps'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        output = result.stdout.decode()
        location = json.loads(output)
        lat = location["latitude"]
        lon = location["longitude"]
        return lat, lon
    except Exception as e:
        raise RuntimeError(f"❌ Gagal mengambil lokasi GPS: {e}")

def get_city_name(lat, lon):
    try:
        geolocator = Nominatim(user_agent="aizahraai")
        location = geolocator.reverse((lat, lon), language='id')
        return location.raw['address'].get('city', 'Kota Tidak Dikenal')
    except:
        return "Kota Tidak Dikenal"

def get_aladhan_data(lat, lon):
    url = f"http://api.aladhan.com/v1/timings?latitude={lat}&longitude={lon}&method=20"
    response = requests.get(url)
    data = response.json()

    if data['code'] != 200:
        raise RuntimeError("❌ Gagal mengambil data dari Aladhan")

    hijri = data['data']['date']['hijri']['date']
    gregorian = data['data']['date']['gregorian']['date']
    weekday = data['data']['date']['gregorian']['weekday']['en']
    timezone = data['data']['meta']['timezone']
    timings = data['data']['timings']

    return {
        "hijri": hijri,
        "gregorian": gregorian,
        "weekday": weekday,
        "timezone": timezone,
        "timings": timings
    }

def speak(text):
    tts = gTTS(text=text, lang='id')
    filename = "/data/data/com.termux/files/home/AizahraAI/suara.mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)

def main():
    print("📡 Mengambil lokasi GPS...")
    lat, lon = get_gps_location()
    print(f"🌍 Lokasi: {lat}, {lon}")

    print("🗺️ Mencari nama kota...")
    city = get_city_name(lat, lon)
    print(f"📍 Kota: {city}")

    print("🕌 Mengambil data dari Aladhan...")
    data = get_aladhan_data(lat, lon)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("⏰ Waktu sekarang:", now)

    # Narasi
    teks = f"""Assalamu'alaikum.
Hari ini {data['weekday']}, tanggal {data['gregorian']} Masehi, bertepatan dengan {data['hijri']} Hijriah.
Waktu lokal sekarang di {city}, zona {data['timezone']}, adalah {now}.
Jadwal sholat:
Subuh pukul {data['timings']['Fajr']},
Terbit pukul {data['timings']['Sunrise']},
Dzuhur pukul {data['timings']['Dhuhr']},
Ashar pukul {data['timings']['Asr']},
Maghrib pukul {data['timings']['Maghrib']},
Isya pukul {data['timings']['Isha']}.
Semoga harimu diberkahi."""

    print("\n📝 Narasi:\n")
    print(teks)
    print("\n🔊 Sedang dibacakan...\n")
    speak(teks)

if __name__ == "__main__":
    main()
