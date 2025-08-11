import json
import os
import time
import subprocess

def play_audio(audio_path):
    try:
        subprocess.run(["mpv", "--no-video", audio_path], check=True)
    except subprocess.CalledProcessError:
        print(f"Gagal memutar audio: {audio_path}")

def play_ayat(surat, ayat, quran_text):
    key = f"{surat}_{ayat}"
    if key not in quran_text:
        print(f"Ayat {key} tidak ditemukan dalam data teks.")
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
        play_audio(audio_path)
        return True
    else:
        print(f"Audio tidak ditemukan: {audio_path}")
        return False

def main():
    with open("data/quran_text.json", "r", encoding="utf-8") as f:
        quran_text = json.load(f)

    surat = 1
    ayat_start = 1
    ayat_end = 7

    for ayat in range(ayat_start, ayat_end + 1):
        success = play_ayat(surat, ayat, quran_text)
        if not success:
            print(f"Berhenti karena ayat {ayat} tidak ditemukan atau audio hilang.")
            break
        time.sleep(1)  # jeda 1 detik antar ayat, bisa diatur

if __name__ == "__main__":
    main()

