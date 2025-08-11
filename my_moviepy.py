# import os  # FIXED: unknown import commented out
os.environ["IMAGEMAGICK_BINARY"] = "/data/data/com.termux/files/usr/bin/magick"

# from moviepy.editor import TextClip  # FIXED: unknown import commented out

clip = TextClip("Halo Termux!", fontsize=70, font="Source-Sans-Pro-Regular", color='white', size=(640,480))
clip = clip.set_duration(5)

clip.write_videofile("output.mp4", fps=24)
