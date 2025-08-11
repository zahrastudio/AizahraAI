# import os  # FIXED: unknown import commented out
# from moviepy.editor import TextClip, CompositeVideoClip  # FIXED: unknown import commented out

# Setting environment ImageMagick path di Termux
os.environ["IMAGEMAGICK_BINARY"] = "/data/data/com.termux/files/usr/bin/magick"

# Buat TextClip sederhana
txt_clip = TextClip("Halo Termux!", fontsize=70, color='white', size=(640, 480))

# Durasi clip 5 detik
txt_clip = txt_clip.set_duration(5)

# Buat video composite (hanya 1 clip)
video = CompositeVideoClip([txt_clip])

# Simpan video
video.write_videofile("output.mp4", fps=24)

print("Video selesai dibuat: output.mp4")
