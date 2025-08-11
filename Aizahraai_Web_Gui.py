from flask import Flask, render_template, request
import subprocess
import json
from datetime import datetime
import requests
# from gtts import gTTS  # FIXED: unknown import commented out
# import os  # FIXED: unknown import commented out
# from geopy.geocoders import Nominatim  # FIXED: unknown import commented out
from get_location import get_location

app = Flask(__name__)

def get_location():
    try:
        result = subprocess.run(["termux-location", "-p", "gps"], capture_output=True, text=True)
        location = json.loads(result.stdout)
        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        return None

def reverse_geocode(lat, lon):
    try:
        geolocator = Nominatim(user_agent="aizahraai")
        location = geolocator.reverse(f"{lat}, {lon}", language='id')
        return location.raw['address'].get('city', 'Kota Tidak Dikenal')
    except:
        return 'Kota Tidak Dikenal'

def get_hijri_and_prayer_times(lat, lon):
    url = f"https://api.aladhan.com/v1/timings/{datetime.now().strftime('%d-%m-%Y')}?latitude={lat}&longitude={lon}&method=2"
    response = requests.get(url).json()
    hijri = response['data']['date']['hijri']['date']
    timings = response['data']['timings']
    return hijri, timings

def generate_narration(city, now, hijri, timings):
    text = f"""Assalamu'alaikum.
Hari ini {now.strftime('%A')}, tanggal {now.strftime('%d-%m-%Y')} Masehi, bertepatan dengan {hijri} Hijriah.
Waktu lokal sekarang di {city}, zona Asia/Jakarta, adalah {now.strftime('%Y-%m-%d %H:%M:%S')}.
Jadwal sholat:
Subuh pukul {timings['Fajr']},
Terbit pukul {timings['Sunrise']},
Dzuhur pukul {timings['Dhuhr']},
Ashar pukul {timings['Asr']},
Maghrib pukul {timings['Maghrib']},
Isya pukul {timings['Isha']}.
Semoga harimu diberkahi."""
    return text

def synthesize_speech(text):
    tts = gTTS(text=text, lang='id')
    filename = "static/audio/narasi.mp3"
    tts.save(filename)

@app.route("/")
def index():
    location = get_location()
    if location:
        lat = location['latitude']
        lon = location['longitude']
        city = reverse_geocode(lat, lon)
        now = datetime.now()
        hijri, timings = get_hijri_and_prayer_times(lat, lon)
        text = generate_narration(city, now, hijri, timings)
        synthesize_speech(text)
        return render_template("index.html", city=city, now=now, hijri=hijri, timings=timings)
    else:
        return "❌ Gagal mengambil lokasi. Pastikan GPS aktif & beri izin Termux."

@app.route("/refresh", methods=["POST"])
def refresh():
    return index()

if __name__ == "__main__":
    app.run(debug=True, port=3000, host='0.0.0.0')


