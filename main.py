
# main.py

from modules.quran import ambil_quran
from gtts import gTTS
import os
from time import sleep

def play(file):
    print(f"▶️ Now Playing: {file}")
    os.system(f"termux-media-player play {file}")
    sleep(1)

def baca_dengan_gtts(arab, latin, arti, prefix="bacaan"):
    if arab:
        print("📜 Arab   :", arab)
        tts_ar = gTTS(text=arab, lang='ar')
        tts_ar.save(f"{prefix}_arab.mp3")
        play(f"{prefix}_arab.mp3")
    else:
        print("⚠️ Teks Arab tidak tersedia.")

    if latin:
        print("🔡 Latin  :", latin)
        tts_lat = gTTS(text=latin, lang='id')
        tts_lat.save(f"{prefix}_latin.mp3")
        play(f"{prefix}_latin.mp3")
    else:
        print("⚠️ Teks Latin tidak tersedia.")

    if arti:
        print("🇮🇩 Arti   :", arti)
        tts_id = gTTS(text=arti, lang='id')
        tts_id.save(f"{prefix}_id.mp3")
        play(f"{prefix}_id.mp3")
    else:
        print("⚠️ Terjemahan tidak tersedia.")

if __name__ == "__main__":
    surah = 1
    ayat = 1

    hasil = ambil_quran(surah, ayat)

    if "error" in hasil:
        print("❌", hasil["error"])
    else:
        print(f"📖 Surah {hasil['surah']} Ayat {hasil['ayat']}")
        baca_dengan_gtts(
            arab=hasil.get("arab", ""),
            latin=hasil.get("latin", ""),
            arti=hasil.get("terjemah", ""),
            prefix=f"quran_{surah}_{ayat}"
        )

