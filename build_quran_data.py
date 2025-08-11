import requests
import json

print("Mengunduh data Al-Qur'an...")
response = requests.get("https://equran.id/api/v2/surat")
data = response.json()["data"]  # ⬅️ Perbaikan penting!

print("Memproses dan menambahkan audio_url...")

quran_data = []

for surah in data:
    nomor_surah = str(surah["nomor"]).zfill(3)
    nama = surah["namaLatin"]
    jumlah_ayat = surah["jumlahAyat"]
    arti = surah["arti"]
    tempat_turun = surah["tempatTurun"]
    deskripsi = surah["deskripsi"]
    audio_full = surah["audioFull"].get("05")  # Misyari-Rasyid

    quran_data.append({
        "nomor": surah["nomor"],
        "nama_latin": nama,
        "jumlah_ayat": jumlah_ayat,
        "arti": arti,
        "tempat_turun": tempat_turun,
        "deskripsi": deskripsi,
        "audio_url": audio_full
    })

with open("quran_data.json", "w", encoding="utf-8") as f:
    json.dump(quran_data, f, ensure_ascii=False, indent=2)

print("✅ Berhasil membuat quran_data.json")

