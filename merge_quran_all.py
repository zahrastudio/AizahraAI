import json

# Load data dari quran_ayat.json
with open("quran_ayat.json", "r", encoding="utf-8") as f:
    ayat_data = json.load(f)

# Load data dari quran_audio_per_ayat.json
with open("quran_audio_per_ayat.json", "r", encoding="utf-8") as f:
    audio_data = json.load(f)

# Load data dari quran_tajwid.json
with open("quran_tajwid.json", "r", encoding="utf-8") as f:
    tajwid_data = json.load(f)

# Indexing audio dan tajwid untuk lookup cepat
audio_lookup = {
    (item["nomor_surah"], item["nomor_ayat"]): item["audio_url"]
    for item in audio_data
}

tajwid_lookup = {
    (item["nomor_surah"], item["nomor_ayat"]): item["tajwid"]
    for item in tajwid_data
}

# Gabungkan semuanya
merged_data = []

for surah in ayat_data:
    nomor_surah = surah["number"]
    nama_surah = surah["name"]

    for ayat in surah["ayat"]:
        nomor_ayat = ayat["number"]
        merged_ayat = {
            "surah": nama_surah,
            "nomor_surah": nomor_surah,
            "nomor_ayat": nomor_ayat,
            "arab": ayat["arab"],
            "latin": ayat["latin"],
            "translation_id": ayat["translation_id"],
            "audio_url": audio_lookup.get((nomor_surah, nomor_ayat), None),
            "tajwid": tajwid_lookup.get((nomor_surah, nomor_ayat), None)
        }
        merged_data.append(merged_ayat)

# Simpan hasil gabungan
with open("quran_all.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print("✅ Berhasil membuat quran_all.json")


