# modules/quran.py

import requests

def ambil_quran(surah_id: int, ayat_id: int):
    url = f"https://api.quran.gading.dev/surah/{surah_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for 4xx/5xx

        data = response.json()

        if "data" not in data:
            return {"error": "Data tidak ditemukan dari API"}

        ayat_list = data["data"].get("verses", [])
        if not ayat_list or not (0 < ayat_id <= len(ayat_list)):
            return {"error": "Ayat tidak ditemukan"}

        ayat_data = ayat_list[ayat_id - 1]

        return {
            "arab": ayat_data["text"].get("arab", ""),
            "latin": ayat_data["text"].get("transliteration", {}).get("id", ""),
            "terjemah": ayat_data.get("translation", {}).get("id", ""),
            "surah": data["data"]["name"].get("transliteration", {}).get("id", ""),
            "ayat": ayat_data["number"].get("inSurah", ayat_id)
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Koneksi gagal: {e}"}
    except Exception as e:
        return {"error": f"Gagal mengambil data: {str(e)}"}



