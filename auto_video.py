# from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip  # FIXED: unknown import commented out

def basic_video():
    text = "Assalamu'alaikum Warahmatullahi Wabarakatuh"
    txt_clip = TextClip(text, fontsize=70, color='white', size=(1280,720), method='caption').set_duration(10)
    audio_clip = AudioFileClip("audio.mp3").set_duration(10)
    video = CompositeVideoClip([txt_clip]).set_audio(audio_clip)
    video.write_videofile("basic_video.mp4", fps=24)

if __name__ == "__main__":
    basic_video()
