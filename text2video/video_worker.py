# video_worker.py
import os, json, threading, subprocess, time, requests
from gtts import gTTS

BASE_DIR = os.path.dirname(__file__)
JOBS_DIR = os.path.join(BASE_DIR, "jobs")
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

os.makedirs(JOBS_DIR, exist_ok=True)

# Simple in-memory queue
_queue = []
_lock = threading.Lock()

def enqueue_job(job_id, text, keyword=None, place=None):
    jobdir = os.path.join(JOBS_DIR, job_id)
    os.makedirs(jobdir, exist_ok=True)
    with open(os.path.join(jobdir, "meta.json"), "w") as f:
        json.dump({"id":job_id, "text":text, "keyword":keyword, "place":place, "status":"queued"}, f)
    with _lock:
        _queue.append(job_id)
    # Ensure worker thread running
    start_worker_thread()

def get_job_status(job_id):
    jobdir = os.path.join(JOBS_DIR, job_id)
    meta = os.path.join(jobdir, "meta.json")
    if not os.path.exists(meta):
        return None
    with open(meta, "r") as f:
        return json.load(f)

# Worker thread
_worker_started = False
def start_worker_thread():
    global _worker_started
    if _worker_started:
        return
    _worker_started = True
    t = threading.Thread(target=_worker_loop, daemon=True)
    t.start()

def _worker_loop():
    while True:
        job_id = None
        with _lock:
            if _queue:
                job_id = _queue.pop(0)
        if job_id:
            try:
                _process_job(job_id)
            except Exception as e:
                _set_status(job_id, "error", error=str(e))
        else:
            time.sleep(1)

def _set_status(job_id, status, **more):
    jobdir = os.path.join(JOBS_DIR, job_id)
    meta_file = os.path.join(jobdir, "meta.json")
    meta = {}
    if os.path.exists(meta_file):
        with open(meta_file, "r") as f:
            meta = json.load(f)
    meta.update({"status":status})
    meta.update(more)
    with open(meta_file, "w") as f:
        json.dump(meta, f)

# helpers: unsplash search
def _unsplash_download(keyword, dest_folder, n=3):
    if not UNSPLASH_KEY:
        return []
    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {UNSPLASH_KEY}"}
    params = {"query": keyword, "per_page": n}
    r = requests.get(url, headers=headers, params=params, timeout=15)
    out=[]
    if r.status_code==200:
        for i,item in enumerate(r.json().get("results",[])):
            img = item["urls"]["regular"]
            fname = os.path.join(dest_folder, f"{keyword.replace(' ','_')}_{i}.jpg")
            try:
                rr = requests.get(img, timeout=20)
                with open(fname,"wb") as f:
                    f.write(rr.content)
                out.append(fname)
            except:
                pass
    return out

def _make_solid_image(path, color="0x283845"):
    # create 1280x720 solid color image
    subprocess.run(["ffmpeg","-y","-f","lavfi","-i", f"color=c={color}:s=1280x720","-frames:v","1", path], check=True)

def _process_job(job_id):
    jobdir = os.path.join(JOBS_DIR, job_id)
    with open(os.path.join(jobdir,"meta.json")) as f:
        meta = json.load(f)
    text = meta.get("text","")
    keyword = meta.get("keyword")
    place = meta.get("place")

    _set_status(job_id, "running")
    # 1) make audio
    audio_path = os.path.join(jobdir,"nar.mp3")
    tts = gTTS(text=text, lang="id")
    tts.save(audio_path)

    # 2) collect images
    imgs = []
    if keyword:
        imgs = _unsplash_download(keyword, jobdir, n=4)
    if not imgs and place:
        imgs = _unsplash_download(place, jobdir, n=3)
    if not imgs:
        fallback = os.path.join(jobdir,"fallback.jpg")
        _make_solid_image(fallback)
        imgs = [fallback]

    # 3) create segments from images
    segment_files=[]
    words = len(text.split())
    per = max(3, min(6, int(max(1, words/len(imgs)/2))))
    for i,img in enumerate(imgs):
        seg = os.path.join(jobdir, f"seg_{i}.mp4")
        cmd = [
            "ffmpeg","-y","-loop","1","-i",img,
            "-c:v","libx264","-t",str(per),
            "-vf","scale=1280:720,format=yuv420p",
            "-r","25", seg
        ]
        subprocess.run(cmd, check=True)
        segment_files.append(seg)

    # 4) concat
    list_txt = os.path.join(jobdir,"list.txt")
    with open(list_txt,"w") as f:
        for s in segment_files:
            f.write(f"file '{os.path.abspath(s)}'\n")
    concat = os.path.join(jobdir,"concat.mp4")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",list_txt,"-c","copy",concat], check=True)

    # 5) mux audio
    final = os.path.join(jobdir,"final.mp4")
    subprocess.run(["ffmpeg","-y","-i", concat, "-i", audio_path, "-c:v","copy","-c:a","aac","-b:a","192k","-shortest", final], check=True)

    _set_status(job_id, "done", output=final)


