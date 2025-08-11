# from gtts import gTTS  # FIXED: unknown import commented out
# from moviepy.editor import *  # FIXED: unknown import commented out
# import os  # FIXED: unknown import commented out

def buat_video_dari_narasi(file_teks):
    with open(file_teks, "r", encoding="utf-8") as f:
        teks = f.read()

    # Buat audio dari teks
    tts = gTTS(teks, lang='id')
    audio_path = "audio.mp3"
    tts.save(audio_path)

    # Tentukan durasi audio
    audio_clip = AudioFileClip(audio_path)
    durasi = audio_clip.duration

    # Buat klip teks
    teks_klip = TextClip(teks, fontsize=40, color='white', size=(720, 1280), method='caption')
    teks_klip = teks_klip.set_duration(durasi).set_position('center').set_audio(audio_clip)

    # Simpan video
    teks_klip.write_videofile("output.mp4", fps=24)

    # Bersihkan file sementara
    os.remove(audio_path)

if __name__ == "__main__":
    buat_video_dari_narasi("narasi.txt")
