import os
import uuid
import requests
import subprocess
from io import BytesIO
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import openai

# Konfigurasi API key dan direktori output
OPENAI_API_KEY = "***REMOVED***proj-uRCupjDZ92B1dzCdD88oC3PnbWdVsfE5TOYyD48zptmYt1Z_eC3eU1WVRkwmdjz2fgOdujMZFQT3BlbkFJld_dvyzsUztPjbXq4GPsNtchwhY0li3sjlwDzIbdPW9Yu9mk99BfaA8url0vbyikhR9kUiuLwA"
UNSPLASH_ACCESS_KEY = "zsTPqex2dLGs5axnNvchotxiLc6b9QYtlS5VFSZcHb4"
OPENAI_API_KEY = "AIzaSyBpWB-1uC3Yiu_3sAvmynXc3ExJnro6KOc"
BASE_DIR = "output"
os.makedirs(BASE_DIR, exist_ok=True)

openai.api_key = OPENAI_API_KEY

app = FastAPI()

class TextRequest(BaseModel):
    prompt: str

def get_keywords(text: str):
    # Mengambil keyword dari OpenAI GPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Extract main keywords from this text:\n\n{text}\n\nKeywords:",
        max_tokens=20,
        temperature=0.3,
    )
    keywords_raw = response.choices[0].text.strip()
    keywords = [k.strip() for k in keywords_raw.split(',')]
    return keywords

def download_image(query: str, index: int):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch images from Unsplash: {resp.text}")
    data = resp.json()
    image_url = data['urls']['regular']
    img_resp = requests.get(image_url)
    img = Image.open(BytesIO(img_resp.content))
    filename = os.path.join(BASE_DIR, f"{query}_{index}.jpg")
    img.save(filename)
    return filename

def create_slideshow(images, output_video, duration_per_image=5):
    list_file = os.path.join(BASE_DIR, "images.txt")
    with open(list_file, "w") as f:
        for img in images:
            f.write(f"file '{img}'\n")
            f.write(f"duration {duration_per_image}\n")
        # ulang frame terakhir supaya video tidak cepat selesai
        f.write(f"file '{images[-1]}'\n")

    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file,
        "-vsync", "vfr", "-pix_fmt", "yuv420p", output_video
    ]
    subprocess.run(cmd, check=True)

def generate_audio(text, audio_file):
    tts = gTTS(text=text, lang='id')
    tts.save(audio_file)

def merge_audio_video(video_file, audio_file, output_file):
    cmd_merge = [
        "ffmpeg", "-i", video_file, "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_file
    ]
    subprocess.run(cmd_merge, check=True)

@app.post("/generate_video/")
async def generate_video(request: TextRequest):
    prompt_text = request.prompt

    # 1. Dapatkan keywords dari teks
    keywords = get_keywords(prompt_text)
    if not keywords:
        raise HTTPException(status_code=400, detail="No keywords extracted from prompt.")

    # 2. Download gambar sesuai keywords
    images = []
    for i, kw in enumerate(keywords):
        try:
            img_path = download_image(kw, i)
            images.append(img_path)
        except Exception as e:
            # Skip jika gagal download
            continue
    if not images:
        raise HTTPException(status_code=500, detail="Failed to download any images.")

    # 3. Buat slideshow video dari gambar
    raw_video = os.path.join(BASE_DIR, f"video_raw_{uuid.uuid4()}.mp4")
    create_slideshow(images, raw_video, duration_per_image=5)

    # 4. Generate audio narasi dari teks
    audio_path = os.path.join(BASE_DIR, f"audio_{uuid.uuid4()}.mp3")
    generate_audio(prompt_text, audio_path)

    # 5. Gabungkan audio dan video
    final_video = os.path.join(BASE_DIR, f"final_video_{uuid.uuid4()}.mp4")
    merge_audio_video(raw_video, audio_path, final_video)

    # Hapus file sementara (opsional)
    try:
        os.remove(raw_video)
        os.remove(audio_path)
        for img in images:
            os.remove(img)
        os.remove(os.path.join(BASE_DIR, "images.txt"))
    except Exception:
        pass

    # Kembalikan link video
    filename = os.path.basename(final_video)
    return {"video_url": f"/video/{filename}"}

@app.get("/video/{filename}")
async def get_video(filename: str):
    file_path = os.path.join(BASE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4", filename=filename)
    return {"error": "File not found"}

