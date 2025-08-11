import os
import subprocess

def download_audio(surat, ayat, query):
    # Buat folder audio jika belum ada
    os.makedirs("audio", exist_ok=True)

    filename = f"audio/quran_{surat}_{ayat}_arab.mp3"

    # Perintah yt-dlp untuk cari dan download audio mp3 video pertama
    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "-x",  # extract audio
        "--audio-format", "mp3",
        "-o", filename,
        "--quiet"
    ]

    print(f"Mencari dan mengunduh: {query}")
    result = subprocess.run(cmd, capture_output=True)

    if result.returncode == 0:
        print(f"Berhasil mengunduh dan menyimpan sebagai {filename}")
        return True
    else:
        print("Gagal mengunduh. Pesan error:")
        print(result.stderr.decode())
        return False

if __name__ == "__main__":
    # Contoh unduh Al-Fatihah ayat 1
    surat = 1
    ayat = 1
    query = "Surah Al-Fatihah Ayat 1 Abdul Basit"

    download_audio(surat, ayat, query)

