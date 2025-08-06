from gtts import gTTS
import os
import arabic_reshaper
from bidi.algorithm import get_display

def format_arabic(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)
def tts_play(teks, lang='id', filename='./temp.mp3'):
    try:
        tts = gTTS(text=teks, lang=lang)
        tts.save(filename)
        os.system(f'termux-media-player play {filename}')
    except Exception as e:
        print("Audio error:", e)


# modules/audio.py

from gtts import gTTS
import os

def tts_gtts(teks, lang='id', filename="output.mp3"):
    try:
        tts = gTTS(text=teks, lang=lang)
        tts.save(filename)
        os.system(f"termux-media-player play {filename}")
        print(f"Now Playing (gTTS): {filename}")
    except Exception as e:
        print(f"TTS error: {e}")

