import os
import shutil

AUDIO_FOLDER = os.path.join(os.getcwd(), "audio")

def ensure_audio_folder():
    if not os.path.exists(AUDIO_FOLDER):
        os.makedirs(AUDIO_FOLDER)

def cleanup_audio_folder():
    ensure_audio_folder()
    for filename in os.listdir(AUDIO_FOLDER):
        file_path = os.path.join(AUDIO_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"⚠️ Gagal menghapus {file_path}: {e}")
    print("🧹 Folder audio dibersihkan.")

