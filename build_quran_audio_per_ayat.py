import json

with open("quran_ayat.json", "r", encoding="utf-8") as f:
    ayat_data = json.load(f)

quran_audio = []

for ayat in ayat_data:
    nomor_surah = str(ayat.get("surah", 1)).zfill(3)  # Gunakan 001 jika tidak ada
    nomor_ayat = str(ayat["number"]).zfill(3)

    # Contoh URL audio per ayat, sesuaikan jika pakai server lain
    audio_url = f"https://verses.quran.com/{nomor_surah}{nomor_ayat}.mp3"

    quran_audio.append({
        "nomor_surah": int(nomor_surah),
        "nomor_ayat": int(nomor_ayat),
        "audio_url": audio_url
    })

with open("quran_audio_per_ayat.json", "w", encoding="utf-8") as f:
    json.dump(quran_audio, f, ensure_ascii=False, indent=2)

print("✅ Berhasil membuat quran_audio_per_ayat.json")

