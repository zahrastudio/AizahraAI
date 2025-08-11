from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from moviepy.video.tools.subtitles import SubtitlesClip

def create_audio(text, lang, filename):
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return filename

def dual_audio_video():
    arabic_text = "بسم الله الرحمن الرحيم"
    indo_text = "Dengan nama Allah Yang Maha Pengasih, Maha Penyayang"
    subtitles = [((0,5), arabic_text), ((5,10), indo_text)]

    # Generate audios
    create_audio(arabic_text, "ar", "arabic.mp3")
    create_audio(indo_text, "id", "indo.mp3")
    bg_music = AudioSegment.from_file("background.mp3").apply_gain(-20)

    arabic_audio = AudioSegment.from_file("arabic.mp3")
    indo_audio = AudioSegment.from_file("indo.mp3")
    combined_audio = bg_music.overlay(arabic_audio)
    combined_audio = combined_audio.overlay(indo_audio, position=len(arabic_audio))

    combined_audio.export("final_audio.mp3", format="mp3")

    # Create video
    txt_clip_ar = TextClip(arabic_text, fontsize=50, color='white').set_duration(5)
    txt_clip_id = TextClip(indo_text, fontsize=50, color='white').set_duration(5).set_start(5)
    video = CompositeVideoClip([txt_clip_ar, txt_clip_id], size=(1280,720))

    # Subtitles
    def subtitle_generator(txt):
        return TextClip(txt, fontsize=24, color='yellow')

    subs = SubtitlesClip(subtitles, subtitle_generator).set_position(("center", "bottom"))

    video = CompositeVideoClip([video, subs])
    video = video.set_audio(AudioFileClip("final_audio.mp3"))

    video.write_videofile("dual_audio_video.mp4", fps=24)

if __name__ == "__main__":
    dual_audio_video()

