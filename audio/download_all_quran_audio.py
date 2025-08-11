import os
import subprocess

def download_audio(surat, ayat, query):
    os.makedirs("audio", exist_ok=True)
    filename = f"audio/quran_{surat}_{ayat}_arab.mp3"
    cmd = [
        "yt-dlp",
        f"ytsearch1:{query}",
        "-x",
        "--audio-format", "mp3",
        "-o", filename,
        "--quiet"
    ]
    print(f"Mengunduh: {query}")
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode == 0:
        print(f"Berhasil: {filename}")
        return True
    else:
        print(f"Gagal mengunduh: {query}")
        return False

if __name__ == "__main__":
    surat = 1
    for ayat in range(1, 8):  # ayat 1 sampai 7
        query = f"Surah Al-Fatihah Ayat {ayat} Abdul Basit"
        download_audio(surat, ayat, query)

