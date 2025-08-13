import os
import tempfile
from gtts import gTTS
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips

def generate_script(prompt: str) -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return "Naskah (fallback): " + prompt
    try:
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{{"role":"user","content":prompt}}])
        return resp.choices[0].message.content
    except Exception as e:
        print("Warning: OpenAI call failed:", e)
        return "Naskah (fallback): " + prompt

def generate_narration(text: str, filename: str = "narration.mp3") -> str:
    tts = gTTS(text=text, lang="id")
    tts.save(filename)
    return filename

def create_slides_from_text(text: str, width=1280, height=720, fontsize=40, duration_per_slide=5):
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paras:
        paras = [text]
    clips = []
    from PIL import Image, ImageDraw, ImageFont
    import textwrap as _tw
    for p in paras:
        img = Image.new("RGB", (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", fontsize)
        except:
            font = ImageFont.load_default()
        wrapped = _tw.fill(p, width=40)
        draw.multiline_text((40, 40), wrapped, font=font, fill=(255,255,255))
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img.save(tmp.name)
        clips.append(ImageClip(tmp.name).set_duration(duration_per_slide))
    return clips

def create_video_from_text(text: str, output: str = "output.mp4") -> str:
    audio_path = generate_narration(text, filename="narration.mp3")
    audio_clip = AudioFileClip(audio_path)
    slides = create_slides_from_text(text, duration_per_slide=max(1, int(audio_clip.duration / max(1, len(text.split('\n\n'))))))
    video = concatenate_videoclips(slides, method="compose")
    video = video.set_audio(audio_clip).set_duration(audio_clip.duration)
    video.write_videofile(output, fps=24, codec='libx264', audio_codec='aac')
    return output
