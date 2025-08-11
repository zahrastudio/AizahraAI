# chatbot.py

from modules.quran import cari_quran
from modules.hadits import cari_hadits
from modules.tts import baca_suara
from rich import print

def tampilkan_quran(hasil):
    print(f"📖 [bold green]{hasil['surah']} {hasil['ayat']}[/]")
    print(f"🕋 Arab   : {hasil['arab']}")
    print(f"🔡 Latin  : {hasil['latin'] or 'Tidak tersedia'}")
    print(f"🇮🇩 Arti   : {hasil['terjemah']}")
    baca_suara(hasil['arab'], hasil['latin'], hasil['terjemah'])

def tampilkan_hadits(hadits):
    print(f"📜 [bold cyan]Hadits[/]")
    print(f"🕋 Arab   : {hadits['arab']}")
    print(f"🔡 Latin  : {hadits['latin'] or 'Tidak tersedia'}")
    print(f"🇮🇩 Arti   : {hadits['terjemah']}")
    baca_suara(hadits['arab'], hadits['latin'], hadits['terjemah'])

def run_chat():
    print("🤖 [bold magenta]AizahraAI Siap Membantu[/]")
    print("Ketik [bold]exit[/] untuk keluar.\n")

    while True:
        user = input("🧑 Kamu: ").strip()
        if not user:
            continue
        if user.lower() == "exit":
            print("👋 Sampai jumpa!")
            break

        # 1. Coba cari dari Al-Qur'an
        hasil = cari_quran(user)
        if hasil:
            tampilkan_quran(hasil)
            continue

        # 2. Coba cari dari Hadits
        hadits = cari_hadits(user)
        if hadits:
            tampilkan_hadits(hadits)
            continue

        # 3. Fallback: tidak ditemukan
        print("🤖 Maaf, saya belum bisa menjawab pertanyaan itu secara umum.")

