# update_cerita.py
import datetime

def update_story():
    # Contoh: tambah narasi berdasarkan tanggal hari ini
    tanggal = datetime.datetime.now().strftime("%Y-%m-%d")
    cerita_baru = f"\n[{tanggal}] Cerita berkembang dengan inspirasi Islami dan kemanusiaan."
    
    with open("cerita.txt", "a", encoding="utf-8") as f:
        f.write(cerita_baru)
    
    print("Cerita diperbarui dengan:", cerita_baru)

if __name__ == "__main__":
    update_story()

