import requests
import json

print("Mengunduh daftar surat...")
surat_list_url = "https://equran.id/api/v2/surat"
response = requests.get(surat_list_url)
surat_list = response.json()["data"]

quran_ayat = []

print("Memproses ayat-ayat tiap surat...")
for surat in surat_list:
    nomor = surat["nomor"]
    nama = surat["namaLatin"]

    detail_url = f"https://equran.id/api/v2/surat/{nomor}"
    res_detail = requests.get(detail_url)
    surat_detail = res_detail.json()["data"]

    ayahs = []
    for ayat in surat_detail["ayat"]:
        ayahs.append({
            "number": ayat["nomorAyat"],
            "arab": ayat["teksArab"],
            "latin": ayat["teksLatin"],
            "translation_id": ayat["teksIndonesia"]
        })

    quran_ayat.append({
        "number": nomor,
        "name": nama,
        "ayahs": ayahs
    })

# Simpan ke file JSON
with open("quran_ayat.json", "w", encoding="utf-8") as f:
    json.dump(quran_ayat, f, ensure_ascii=False, indent=2)

print("✅ Berhasil membuat quran_ayat.json")

