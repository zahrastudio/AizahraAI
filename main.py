# main.py

from modules.quran import ambil_quran
from gtts import gTTS
import os
from time import sleep

def play(file):
    print("▶️", file)
    os.system(f"termux-media-player play {file}")
    sleep(1)

def baca_dengan_gtts(arab, latin, arti, prefix="bacaan"):
    print("📜 Arab   :", arab)
    tts_ar = gTTS(text=arab, lang='ar')
    tts_ar.save(f"{prefix}_arab.mp3")
    play(f"{prefix}_arab.mp3")

    print("🔡 Latin  :", latin)
    tts_lat = gTTS(text=latin, lang='id')
    tts_lat.save(f"{prefix}_latin.mp3")
    play(f"{prefix}_latin.mp3")

    print("🇮🇩 Arti   :", arti)
    tts_id = gTTS(text=arti, lang='id')
    tts_id.save(f"{prefix}_id.mp3")
    play(f"{prefix}_id.mp3")

# Contoh pemanggilan
if __name__ == "__main__":
    hasil = ambil_quran(1, 1)  # Al-Fatihah ayat 1
    if "error" in hasil:
        print("❌", hasil["error"])
    else:
        baca_dengan_gtts(hasil["arab"], hasil["latin"], hasil["terjemah"], prefix=f"{hasil['surah']}_{hasil['ayat']}")

