import json
import os
import time
from playsound import playsound

with open("data/quran_text.json", "r", encoding="utf-8") as f:
    quran_text = json.load(f)

def play_ayat(surat, ayat):
    key = f"{surat}_{ayat}"
    if key not in quran_text:
        print("Ayat tidak ditemukan.")
        return False

    arab = quran_text[key]["arab"]
    latin = quran_text[key]["latin"]
    arti = quran_text[key]["id"]

    print(f"\n📖 Surah {surat} Ayat {ayat}")
    print(f"📜 Arab   : {arab}")
    print(f"⚠️ Latin  : {latin}")
    print(f"🇮🇩 Arti   : {arti}")

    audio_path = f"audio/quran_{surat}_{ayat}_arab.mp3"
    if os.path.exists(audio_path):
        print(f"▶️ Now Playing: {audio_path}")
        playsound(audio_path)
        return True
    else:
        print("Audio tidak ditemukan:", audio_path)
        return False

def main():
    surat = 1
    for ayat in range(1, 8):
        played = play_ayat(surat, ayat)
        if not played:
            break
        time.sleep(1)

if __name__ == "__main__":
    main()

