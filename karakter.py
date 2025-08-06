
data = {
    "zahra": {
        "nama": "Zahra",
        "peran": "Tokoh utama wanita",
        "kutipan": "Langit adalah saksi dari hati yang belum selesai."
    },
    "raihan": {
        "nama": "Raihan",
        "peran": "Penulis & aktivis",
        "kutipan": "Cinta tak usai meski langit berubah."
    }
}

def kenali_karakter(nama):
    k = data.get(nama.lower())
    if not k: return False
    print(f"Nama: {k['nama']}\nPeran: {k['peran']}\nKutipan: \"{k['kutipan']}\"")
    return True


