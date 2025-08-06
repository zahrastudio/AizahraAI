import requests
import os
import json
import time
from gtts import gTTS

# === API Key ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "ISI_API_KEY_KAMU"

# === Header GPT ===
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

# === BASMALAH ===
def ucap_basmallah():
    print("📖 بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ")
    print("📖 Bismillāhir-raḥmānir-raḥīm")
    print("📖 Dengan nama Allah Yang Maha Pengasih lagi Maha Penyayang")
    tts = gTTS("Bismillahirrahmanirrahim. Dengan hormat, aku Aizahra. Ada yang ingin kamu tanyakan?", lang='id')
    tts.save("bismillah.mp3")
    os.system("termux-media-player play bismillah.mp3")

# === QURAN FEATURE ===
def tampilkan_ayat(surat, ayat):
    url = f"https://equran.id/api/surat/{surat}/{ayat}"
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        teks_arab = data['arab']
        teks_latin = data['latin']
        teks_indo = data['idn']
        audio = data['audio']

        print("\n📖 AYAT AL-QUR’AN")
        print("📖 Lafaz Arab       :", teks_arab)
        print("📖 Transliterasi    :", teks_latin)
        print("📖 Terjemahan ID    :", teks_indo)

        filename = "ayat.mp3"
        audio_file = requests.get(audio)
        with open(filename, 'wb') as f:
            f.write(audio_file.content)
        os.system(f"termux-media-player play {filename}")
        time.sleep(2)

    except Exception as e:
        print("⚠️ Gagal mengambil ayat:", str(e))

# === DETEKSI PERINTAH BACA ALQURAN ===
def deteksi_perintah_quran(teks):
    teks = teks.lower()
    if "baca" in teks and "ayat" in teks:
        try:
            # contoh: baca al-kahfi ayat 10 → ambil nomor surat & ayat
            parts = teks.replace("baca", "").strip().split("ayat")
            nama = parts[0].strip()
            ayat = int(parts[1].strip())

            # mapping nama surat ke nomor
            daftar_surat = {
                "al-fatihah": 1, "al-baqarah": 2, "ali-imran": 3, "an-nisa": 4, "al-kahfi": 18
                # tambah surat lain sesuai kebutuhan
            }

            surat = daftar_surat.get(nama)
            if surat:
                tampilkan_ayat(surat, ayat)
                return True
            else:
                print("⚠️ Surat tidak dikenali.")
                return False
        except:
            print("⚠️ Format tidak dikenali.")
            return False
    return False

# === TANYA GPT ===
def tanya_aizahra(pertanyaan):
    pesan = [
        {"role": "system", "content": "Kamu adalah Aizahra, asisten Islami yang lembut dan edukatif."},
        {"role": "user", "content": pertanyaan}
    ]
    data = {"model": "gpt-3.5-turbo", "messages": pesan}

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
        response.raise_for_status()
        hasil = response.json()
        return hasil['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# === MAIN LOOP ===
ucap_basmallah()

while True:
    user_input = input("\n🧕 Kamu: ")
    if user_input.lower() in ["exit", "keluar", "quit"]:
        print("📖 وَٱللَّهُ أَعْلَمُ بِٱلصَّوَابِ")
        print("📖 Wallāhu a‘lamu biṣ-ṣawāb")
        print("📖 Dan Allah-lah yang lebih mengetahui kebenaran yang sebenar-benarnya 🌸")
        break

    if not deteksi_perintah_quran(user_input):
        jawaban = tanya_aizahra(user_input)
        print(f"\n🤖 Aizahra: {jawaban.strip()}")
        print("📖 وَٱللَّهُ أَعْلَمُ بِٱلصَّوَابِ")
        print("📖 Wallāhu a‘lamu biṣ-ṣawāb")
        print("📖 Dan Allah-lah yang lebih mengetahui kebenaran yang sebenar-benarnya 🌸")

