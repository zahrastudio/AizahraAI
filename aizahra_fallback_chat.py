#!/usr/bin/env python3
"""
AIzahraAI - Chat assistant with OpenAI primary mode and local fallback.
Save as: aizahra_fallback_chat.py
Run: python aizahra_fallback_chat.py
"""

# import os, sys, time, json  # FIXED: unknown import commented out
# from dotenv import load_dotenv  # FIXED: unknown import commented out
import requests
# from gtts import gTTS  # FIXED: unknown import commented out
import glob
# from pathlib import Path  # FIXED: unknown import commented out

# try import optional libs
try:
    import numpy as np
except Exception:
    np = None

USE_SKLEARN = False
try:
#     from sklearn.feature_extraction.text import TfidfVectorizer  # FIXED: unknown import commented out
#     from sklearn.metrics.pairwise import cosine_similarity  # FIXED: unknown import commented out
    USE_SKLEARN = True
except Exception:
    USE_SKLEARN = False

# Load .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Config
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-3.5-turbo"   # change if you want
KNOWLEDGE_DIR = Path("knowledge")
AUDIO_DIR = Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
CONVERSATION_LOG = "conversation.log"

# -- Utilities ---------------------------------------------------------------
def speak_and_save(text, filename="narration.mp3", lang="id"):
    out = AUDIO_DIR / filename
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(str(out))
    except Exception as e:
        print("⚠️ TTS error:", e)
        return None
    # try play (termux/media-player) - best-effort:
    try:
        os.system(f"termux-media-player play {out} >/dev/null 2>&1 &")
    except Exception:
        pass
    return str(out)

def log_exchange(role, text):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(CONVERSATION_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {role}: {text}\n")

# -- OpenAI call -------------------------------------------------------------
def ask_openai(system_prompt, user_prompt):
    if not OPENAI_KEY:
        raise RuntimeError("No OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.6,
        "max_tokens": 800
    }
    try:
        resp = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=30)
    except Exception as e:
        raise RuntimeError(f"Network/API error: {e}")
    if resp.status_code == 401:
        raise RuntimeError("Unauthorized: invalid OpenAI API key (401).")
    if resp.status_code >= 400:
        raise RuntimeError(f"OpenAI API returned {resp.status_code}: {resp.text}")
    j = resp.json()
    return j["choices"][0]["message"]["content"].strip()

# -- Local knowledge loader & retriever -------------------------------------
def load_local_documents():
    docs = []
    for p in sorted(KNOWLEDGE_DIR.glob("**/*.txt")):
        try:
            txt = p.read_text(encoding="utf-8")
        except:
            txt = p.read_text(encoding="latin-1")
        docs.append({"path": str(p), "text": txt})
    return docs

def build_tfidf_index(docs):
    texts = [d["text"] for d in docs]
    if USE_SKLEARN:
        vect = TfidfVectorizer(stop_words="english").fit_transform(texts)
        return {"type": "sklearn", "vec": vect, "texts": texts, "docs": docs}
    else:
        # fallback: store raw texts (will use difflib)
        return {"type": "simple", "texts": texts, "docs": docs}

# from difflib import SequenceMatcher, get_close_matches  # FIXED: unknown import commented out
def simple_retrieve(index, query, top_k=3):
    if index["type"] == "sklearn" and np is not None:
        q_vect = TfidfVectorizer(stop_words="english").fit(index["texts"]).transform([query])
        sims = cosine_similarity(q_vect, index["vec"]).flatten()
        ranked = np.argsort(-sims)[:top_k]
        results = []
        for r in ranked:
            score = float(sims[r])
            if score <= 0: continue
            results.append({"score": score, "path": index["docs"][r]["path"], "text": index["texts"][r]})
        return results
    else:
        # difflib-based similarity on joined texts (cheap)
        scores = []
        for i, t in enumerate(index["texts"]):
            sm = SequenceMatcher(None, query, t)
            score = sm.quick_ratio()
            scores.append((score, i))
        scores.sort(reverse=True)
        results = []
        for score, i in scores[:top_k]:
            if score <= 0.05: continue
            results.append({"score": score, "path": index["docs"][i]["path"], "text": index["texts"][i]})
        return results

def compose_local_answer(query, index):
    hits = simple_retrieve(index, query, top_k=4)
    if not hits:
        return ("Maaf, saya tidak menemukan jawaban yang relevan pada koleksi lokal. "
                "Coba periksa koneksi OpenAI atau tambahkan dokumen ke folder `knowledge/`.")
    # simple composition: take top passages and summarize (concatenate)
    out = []
    for h in hits:
        snippet = h["text"].strip()
        # truncate long text
        if len(snippet) > 800:
            snippet = snippet[:800].rsplit("\n",1)[0] + "..."
        out.append(f"(Sumber: {Path(h['path']).name})\n{snippet}")
    return "\n\n".join(out)

# -- Optionally call local LLM (gpt4all) ------------------------------------
def call_local_llm(prompt):
    """If you installed gpt4all / local binary, you can integrate here.
       This is a stub - try: subprocess.run(['gpt4all', '-p', prompt]) or similar."""
    try:
        import subprocess, shlex
        # Example: gpt4all-lora or gpt4all binary must be in PATH.
        cmd = f"gpt4all -m ./models/gpt4all-lora.bin -p {shlex.quote(prompt)}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return None

# -- Main interactive loop --------------------------------------------------
def main():
    print("AIzahraAI - chat (OpenAI primary, local fallback).")
    print("Tip: letakkan file teks di folder 'knowledge/' untuk meningkatkan fallback.")
    docs = load_local_documents()
    if docs:
        print(f"📚 {len(docs)} dokumen lokal ditemukan di knowledge/")
    index = build_tfidf_index(docs)

    system_prompt = ("Kamu adalah AIzahraAI - asisten ramah, ringkas, dan penuh empati. "
                     "Jika menggunakan local fallback, jawaban harus menyertakan sumber dokumen lokal bila ada.")
    while True:
        try:
            user = input("\nKamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar. Sampai jumpa.")
            break
        if not user:
            continue
        if user.lower() in ("exit","quit","bye"):
            print("Sampai jumpa.")
            break

        # Try OpenAI first
        answer = None
        used_mode = "openai"
        if OPENAI_KEY:
            try:
                answer = ask_openai(system_prompt, user)
            except Exception as e:
                print("⚠️ OpenAI error - beralih ke fallback lokal:", e)
                used_mode = "fallback"
        else:
            used_mode = "fallback"

        if used_mode == "fallback":
            # First try local LLM if available
            local_llm_out = call_local_llm(user)
            if local_llm_out:
                answer = local_llm_out
            else:
                answer = compose_local_answer(user, index)

        # Log + speak
        log_exchange("User", user)
        log_exchange("AI", answer)
        print("\nAIzahraAI:", answer)
        speak_and_save(answer, filename=f"narration_{int(time.time())}.mp3", lang="id")

if __name__ == "__main__":
    main()
