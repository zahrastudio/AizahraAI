import json
# import re  # FIXED: unknown import commented out

# Fungsi identifikasi tajwid sederhana (masih dasar)
def deteksi_tajwid(arab_text):
    rules = {
        "idgham": r"نْ(?=\s*[يرملون])",
        "ikhfa": r"نْ(?=\s*[تثجدذزسشصضطظفكق])",
        "idzhar": r"نْ(?=\s*[ءهعغحخ])",
        "qalqalah": r"[بجدطق](?=ْ)",  # huruf qalqalah sukun
        # Tambah aturan lainnya sesuai kebutuhan
    }

    hasil = []
    for hukum, pattern in rules.items():
        if re.search(pattern, arab_text):
            hasil.append(hukum)
    return hasil

# Load quran_ayat.json
with open("quran_ayat.json", "r", encoding="utf-8") as f:
    data_ayat = json.load(f)

# Proses setiap ayat dan tandai tajwid
tajwid_data = []

for surah in data_ayat:
    surah_number = surah["number"]
    for ayat in surah["ayahs"]:
        tajwid_found = deteksi_tajwid(ayat["arab"])
        tajwid_data.append({
            "nomor_surah": surah_number,
            "nomor_ayat": ayat["number"],
            "tajwid": tajwid_found
        })

# Simpan ke file
with open("quran_tajwid.json", "w", encoding="utf-8") as f:
    json.dump(tajwid_data, f, indent=2, ensure_ascii=False)

print("✅ Berhasil membuat quran_tajwid.json")
