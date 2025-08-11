#!/bin/bash

# Update & install paket dasar
pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git nano

# Setup Python virtual environment
python -m pip install --upgrade pip
pip install virtualenv
python -m virtualenv ~/aizahraai_env

# Aktifkan virtualenv
source ~/aizahraai_env/bin/activate

# Install dependencies Python
pip install fastapi uvicorn moviepy requests gTTS

# Buat folder kerja output
mkdir -p ~/aizahraai_output/frames
mkdir -p ~/aizahraai_output/audio

echo "Setup selesai. Virtualenv aktif, dependencies terpasang."

# Contoh script Python sederhana buat frames dummy + gabung audio jadi video

cat > ~/aizahraai.py <<EOF
import os
from moviepy.editor import ImageSequenceClip, AudioFileClip
from gtts import gTTS

OUT_DIR = os.path.expanduser("~/aizahraai_output")
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
AUDIO_PATH = os.path.join(OUT_DIR, "audio", "narasi.mp3")
VIDEO_PATH = os.path.join(OUT_DIR, "output.mp4")

def generate_dummy_frames(num_frames=10):
    # buat dummy frames hitam dengan teks nomor frame
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(FRAMES_DIR, exist_ok=True)
    for i in range(num_frames):
        img = Image.new("RGB", (640, 360), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        text = f"Frame {i+1}"
        # font default
        draw.text((250, 170), text, fill=(255,255,255))
        img.save(os.path.join(FRAMES_DIR, f"frame_{i:03d}.png"))

def generate_audio(text="Ini adalah contoh narasi AizahraAI"):
    os.makedirs(os.path.dirname(AUDIO_PATH), exist_ok=True)
    tts = gTTS(text, lang="id")
    tts.save(AUDIO_PATH)

def compose_video():
    frames = sorted([os.path.join(FRAMES_DIR, f) for f in os.listdir(FRAMES_DIR) if f.endswith(".png")])
    clip = ImageSequenceClip(frames, fps=2)
    audio = AudioFileClip(AUDIO_PATH)
    clip = clip.set_audio(audio)
    clip.write_videofile(VIDEO_PATH, codec="libx264", audio_codec="aac")
    print(f"Video tersimpan di {VIDEO_PATH}")

if __name__ == "__main__":
    generate_dummy_frames(10)
    generate_audio("Selamat datang di AizahraAI, aplikasi AI teks ke video.")
    compose_video()
EOF

echo "Contoh script Python telah dibuat di ~/aizahraai.py"
echo "Jalankan script dengan: source ~/aizahraai_env/bin/activate && python ~/aizahraai.py"
