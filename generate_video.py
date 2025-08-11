import os
os.environ['IMAGEMAGICK_BINARY'] = '/data/data/com.termux/files/usr/bin/magick'

from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

def generate_video_from_text(file_path="cerita.txt", output_path="output.mp4"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    bg = ColorClip(size=(720, 480), color=(20, 20, 40), duration=10)

    clip = TextClip(text, fontsize=24, color='white', font='Roboto', size=(700, None), method='caption')
    clip = clip.set_position('center').set_duration(10)

    video = CompositeVideoClip([bg, clip])
    video.write_videofile(output_path, fps=24)

    print("Video telah dibuat:", output_path)

if __name__ == "__main__":
    generate_video_from_text()

