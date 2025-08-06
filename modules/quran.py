# modules/quran.py
import requests

def ambil_quran(surah_id: int, ayat_id: int):
    url = f"https://api.quran.gading.dev/surah/{surah_id}"

    try:
        response = requests.get(url)
        data = response.json()

        if "data" in data:
            ayat_list = data["data"]["verses"]

            if 0 < ayat_id <= len(ayat_list):
                ayat_data = ayat_list[ayat_id - 1]
                arabic = ayat_data["text"]["arab"]
                latin = ayat_data["text"]["transliteration"]["id"]
                translation = ayat_data["translation"]["id"]
                return {
                    "arab": arabic,
                    "latin": latin,
                    "terjemah": translation,
                    "surah": data["data"]["name"]["transliteration"]["id"],
                    "ayat": ayat_data["number"]["inSurah"]
                }
            else:
                return {"error": "Ayat tidak ditemukan"}
        else:
            return {"error": "Data tidak ditemukan dari API"}
    except Exception as e:
        return {"error": f"Gagal mengambil data: {str(e)}"}

