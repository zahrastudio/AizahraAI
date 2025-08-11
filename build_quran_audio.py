import json

with open("quran_ayat.json", "r", encoding="utf-8") as f:
    data = json.load(f)

quran_audio = []

for surah in data:
    nomor_surah = str(surah["number"]).zfill(3)
    nama_surah = surah["name"]

    for ayat in surah["ayahs"]:  # ← Pastikan ini sesuai dengan struktur list di dalam
        nomor_ayat = str(ayat["number"]).zfill(3)
        audio_url = f"https://equran.nos.wjv-1.neo.id/audio-full/Misyari-Rasyid-Al-Afasi/{nomor_surah}.mp3"

        quran_audio.append({
            "surah": nama_surah,
            "nomor_surah": int(surah["number"]),
            "nomor_ayat": int(ayat["number"]),
            "audio_url": audio_url
        })

with open("quran_audio.json", "w", encoding="utf-8") as f:
    json.dump(quran_audio, f, ensure_ascii=False, indent=2)

print("✅ Berhasil membuat quran_audio.json")

