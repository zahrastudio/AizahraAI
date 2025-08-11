# from moviepy.editor import *  # FIXED: unknown import commented out
# from gtts import gTTS  # FIXED: unknown import commented out
# from dotenv import load_dotenv  # FIXED: unknown import commented out
# import os  # FIXED: unknown import commented out
import requests

# ✅ Load .env
load_dotenv()
PIXABAY_KEY = os.getenv("PIXABAY_API_KEY")

# 📝 Teks narasi
narration_text = """
Di masa depan, teknologi membantu manusia menghadapi perubahan iklim.
"""

# 🎤 TTS
tts = gTTS(narration_text, lang='id')
tts.save("voice.mp3")

# 🔍 Ambil kata kunci pencarian dari kalimat pertama
search_query = narration_text.strip().split(".")[0].replace(" ", "+")

# 🔍 Fungsi cari gambar Pixabay
def get_pixabay_image(query, key):
    url = f"https://pixabay.com/api/?key={key}&q={query}&image_type=photo&orientation=horizontal&per_page=3"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "hits" in data and len(data["hits"]) > 0:
            return data["hits"][0]["largeImageURL"]
    except Exception as e:
        print(f"⚠️ Pixabay error: {e}")
    return None

# 📥 Download gambar dari URL
def download_image(url, filename):
    try:
        img_data = requests.get(url, timeout=10).content
        with open(filename, "wb") as f:
            f.write(img_data)
        return filename
    except Exception as e:
        print(f"⚠️ Gagal download gambar: {e}")
        return None

# 📥 Coba pakai Pixabay
image_url = get_pixabay_image(search_query, PIXABAY_KEY)
image_file = download_image(image_url, "downloaded.jpg") if image_url else None

# 🎞️ Ambil background clip
def load_background(duration):
    if image_file and os.path.exists(image_file):
        print("✅ Menggunakan gambar dari Pixabay")
        return ImageClip(image_file).set_duration(duration).resize(height=720)
    elif os.path.exists("fallback.jpg"):
        print("⚠️ Fallback: menggunakan fallback.jpg lokal")
        return ImageClip("fallback.jpg").set_duration(duration).resize(height=720)
    else:
        raise FileNotFoundError("❌ Tidak ditemukan gambar dari Pixabay maupun fallback.jpg")

# 🎧 Audio
audio = AudioFileClip("voice.mp3")
duration = audio.duration

# 🖼️ Background
background = load_background(duration).set_audio(audio)

# 📝 Tambahkan teks ke video
text_clip = TextClip(narration_text.strip(), fontsize=38, color='white', font='DejaVu-Sans',
                     method='caption', size=(1000, None)).set_position(("center", "bottom")).set_duration(duration)

# 🔄 Gabungkan semuanya
final_video = CompositeVideoClip([background, text_clip])

# 💾 Simpan ke MP4
final_video.write_videofile("film_output.mp4", fps=24)
