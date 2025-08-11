#!/usr/bin/env python3
"""
updater.py
Automate fetching Quran data (ayat/audio/tajwid), build JSON files,
and optionally commit & push to git or upload to GitHub/Stoplight.

Designed for Termux / Linux environment.

Usage:
    python updater.py
"""

# import os  # FIXED: unknown import commented out
# import sys  # FIXED: unknown import commented out
import json
# import time  # FIXED: unknown import commented out
import logging
import subprocess
from datetime import datetime
# from pathlib import Path  # FIXED: unknown import commented out

import requests
# from dotenv import load_dotenv  # FIXED: unknown import commented out

# -------------------------
# Config & Environment
# -------------------------
ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

# Endpoints (adjust if you prefer other providers)
SURAH_LIST_URL = "https://equran.id/api/v2/surat"
SURAH_DETAIL_URL = "https://equran.id/api/v2/surat/{id}"   # {id} -> surah number

# Options
OUT_DIR = ROOT  # output files will be created here
OUT_QAYAT = OUT_DIR / "quran_ayat.json"
OUT_AUDIO_PER_AYAT = OUT_DIR / "quran_audio_per_ayat.json"
OUT_TAJWID = OUT_DIR / "quran_tajwid.json"

# Git / GitHub settings from .env
GIT_REMOTE = os.getenv("GIT_REMOTE", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
COMMIT_AUTHOR_NAME = os.getenv("COMMIT_AUTHOR_NAME", "AizahraAI")
COMMIT_AUTHOR_EMAIL = os.getenv("COMMIT_AUTHOR_EMAIL", "aizahra@example.com")

# Stoplight placeholder
STOPLIGHT_TOKEN = os.getenv("STOPLIGHT_TOKEN", "")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


# -------------------------
# Utilities
# -------------------------
def http_get_json(url, params=None, headers=None, timeout=20):
    try:
        r = requests.get(url, params=params, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error("HTTP GET failed for %s - %s", url, e)
        return None


def safe_write_json(path: Path, obj):
    path_tmp = path.with_suffix(path.suffix + ".tmp")
    with open(path_tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    path_tmp.replace(path)
    logging.info("Wrote %s (%d bytes)", path.name, path.stat().st_size)


# -------------------------
# Fetch & Build Functions
# -------------------------
def fetch_surah_list():
    logging.info("Fetching surah list from %s", SURAH_LIST_URL)
    data = http_get_json(SURAH_LIST_URL)
    if not data:
        raise RuntimeError("Failed to fetch surah list")
    # equran.id returns a structure - adapt to actual response shape
    # Many public endpoints return {"data": [...]}
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    # fallback if endpoint returns list
    if isinstance(data, list):
        return data
    raise RuntimeError("Unexpected surah list format")


def fetch_surah_detail(surah_id):
    url = SURAH_DETAIL_URL.format(id=surah_id)
    logging.info("Fetching surah detail %s", url)
    data = http_get_json(url)
    if not data:
        raise RuntimeError(f"Failed to fetch surah {surah_id}")
    # common wrapper: {"data": {...}}
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data


def build_quran_ayat_and_tajwid():
    """
    Build 2 JSON outputs:
    - quran_ayat.json: [{ "number":1, "name":"Al-Fatihah", "verses":[{number, arab, latin, translation_id}, ...]}, ...]
    - quran_tajwid.json: similar but includes arab_tajwid (if endpoint provides)
    - quran_audio_per_ayat.json: [{nomor_surah, nomor_ayat, audio_url}, ...] (constructed from available audioFull or pattern)
    """
    surah_list = fetch_surah_list()
    quran_ayat = []
    quran_tajwid = []
    audio_entries = []

    for s in surah_list:
        # adapt to available keys: equran id returns e.g. {"nomor": 1, "nama": "...", ...}
        # Try several possible keys to be robust
        number = s.get("nomor") or s.get("number") or s.get("nomor_surah") or s.get("id")
        if number is None:
            logging.warning("Surah entry missing number key: %s", s.keys())
            continue
        number = int(number)

        # get detail (verses)
        try:
            detail = fetch_surah_detail(number)
        except Exception as e:
            logging.error("Skipping surah %s due to error: %s", number, e)
            continue

        # surah meta names - adapt for different key names
        name = detail.get("nama") or detail.get("name") or detail.get("name_simple") or detail.get("englishName") or detail.get("namaLatin") or str(number)

        verses = []
        verses_tajwid = []

        # detail often contains "ayat" or "verses" or "verses" nested in "verses"
        raw_verses = None
        if isinstance(detail, dict):
            raw_verses = detail.get("ayat") or detail.get("verses") or detail.get("ayatList") or detail.get("versesList")
        if raw_verses is None and isinstance(detail, list):
            raw_verses = detail
        if raw_verses is None:
            logging.warning("No verses found for surah %s", number)
            raw_verses = []

        for ay in raw_verses:
            # determine numbering and fields
            ay_no = None
            if isinstance(ay, dict):
                # common shapes from equran.id: ay["nomor"] or ay["number"]["inSurah"]
                ay_no = ay.get("nomor") or (ay.get("number") and ay["number"].get("inSurah")) or ay.get("number") or ay.get("verse") or ay.get("ayat")
                arab = None
                latin = None
                translation_id = None
                arab_tajwid = None

                # try patterns for arab text & transliteration & translation
                if "text" in ay and isinstance(ay["text"], dict):
                    # e.g. ay["text"]["arab"], ay["text"]["transliteration"]["id"], ay["translation"]["id"]
                    arab = ay["text"].get("arab") or ay.get("arab")
                    # latin may be at ay["text"]["transliteration"] or elsewhere
                    try:
                        latin = ay["text"].get("transliteration", {}).get("id") or ay["text"].get("transliteration", {}).get("en") or ay.get("latin")
                    except Exception:
                        latin = None
                else:
                    arab = ay.get("arab") or ay.get("text") or None
                    latin = ay.get("latin") or None

                # translation
                translation_id = (
                    (ay.get("translation") and ay["translation"].get("id"))
                    or (ay.get("terjemah") or ay.get("translation_id") or ay.get("translation"))
                )

                # tajwid (some endpoints include tajwid/arab_tajwid)
                arab_tajwid = ay.get("text", {}).get("arab_tajwid") if isinstance(ay.get("text"), dict) else ay.get("arab_tajwid") or None

                if isinstance(ay_no, dict):
                    # sometimes number field is nested
                    # look for "inSurah" or "number"
                    ay_no = ay_no.get("inSurah") or ay_no.get("number") or None

                try:
                    ay_no = int(ay_no) if ay_no is not None else None
                except Exception:
                    ay_no = None

                # fallback defaults
                verses.append({
                    "number": ay_no,
                    "arab": arab,
                    "latin": latin,
                    "translation_id": translation_id
                })
                verses_tajwid.append({
                    "number": ay_no,
                    "arab": arab,
                    "arab_tajwid": arab_tajwid,
                    "latin": latin,
                    "translation_id": translation_id
                })

                # audio: try to use audioFull map or predictable pattern if available
                # If detail has "audioFull" or "audio" block
                # Many equran endpoints include detail["audioFull"] mapping with keys "01","02",...
                audio_map = detail.get("audioFull") or detail.get("audio_full") or detail.get("audio")
                if isinstance(audio_map, dict):
                    # audio_map might be {"01":"https://.../001.mp3", ...}
                    key = str(ay_no).zfill(2) if ay_no is not None else None
                    # some use two-digit keys or three-digit zero padded
                    audio_url = None
                    if key:
                        if key in audio_map:
                            audio_url = audio_map[key]
                        else:
                            # try zero padded 3
                            audio_url = audio_map.get(str(ay_no).zfill(3)) or audio_map.get(str(ay_no))
                    if audio_url:
                        audio_entries.append({
                            "nomor_surah": number,
                            "nomor_ayat": ay_no,
                            "audio_url": audio_url
                        })

            else:
                # if ay is primitive (unlikely) - skip
                continue

        quran_ayat.append({
            "number": number,
            "name": name,
            "verses": verses
        })
        quran_tajwid.append({
            "number": number,
            "name": name,
            "verses": verses_tajwid
        })

        # If audio_entries is still empty for the whole surah, try to infer per-ayat audio via pattern:
        # many CDNs have pattern like https://equran.nos.wjv-1.neo.id/audio-full/<reciter>/<NNN.mp3>
        # We will not invent unknown reciters; rely on audio_map above.

    # Done all surahs
    return quran_ayat, quran_tajwid, audio_entries


# -------------------------
# Git operations
# -------------------------
def git_commit_and_push(files, message=None):
    """Commit and push changes using local git. Repo must be configured."""
    try:
        if message is None:
            message = f"Auto update quran data: {datetime.utcnow().isoformat()}Z"
        # stage files
        cmd_add = ["git", "add"] + [str(p) for p in files]
        subprocess.run(cmd_add, check=True, cwd=ROOT)
        # commit
        env = os.environ.copy()
        env["GIT_AUTHOR_NAME"] = COMMIT_AUTHOR_NAME
        env["GIT_AUTHOR_EMAIL"] = COMMIT_AUTHOR_EMAIL
        env["GIT_COMMITTER_NAME"] = COMMIT_AUTHOR_NAME
        env["GIT_COMMITTER_EMAIL"] = COMMIT_AUTHOR_EMAIL
        subprocess.run(["git", "commit", "-m", message], check=True, cwd=ROOT, env=env)
        # push (assumes remote origin configured and credentials available)
        subprocess.run(["git", "push"], check=True, cwd=ROOT)
        logging.info("Git push successful")
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Git operation failed: %s", e)
        return False


# -------------------------
# Optionally: GitHub API upload (fallback)
# -------------------------
def upload_file_to_github_api(path: Path, repo_full_name: str, branch="main"):
    """
    Create or update a file via GitHub Contents API.
    repo_full_name: e.g. 'username/repo'
    Requires GITHUB_TOKEN in env.
    """
    if not GITHUB_TOKEN:
        logging.warning("GITHUB_TOKEN not set - skipping GitHub upload for %s", path)
        return False
    url = f"https://api.github.com/repos/{repo_full_name}/contents/{path.name}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    # get existing file to find sha
    r = requests.get(url + f"?ref={branch}", headers=headers)
    sha = None
    if r.status_code == 200:
        sha = r.json().get("sha")
    content_b64 = Path(path).read_bytes().encode("base64") if False else None
    # simpler: use text content and base64 encode
#     import base64  # FIXED: unknown import commented out
    content_b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    body = {
        "message": f"Auto update {path.name}",
        "content": content_b64,
        "branch": branch
    }
    if sha:
        body["sha"] = sha
    r2 = requests.put(url, json=body, headers=headers)
    if r2.status_code in (200, 201):
        logging.info("Uploaded %s to GitHub (repo %s)", path.name, repo_full_name)
        return True
    else:
        logging.error("GitHub upload failed: %s %s", r2.status_code, r2.text)
        return False


# -------------------------
# Stoplight placeholder
# -------------------------
def update_stoplight(openapi_url: str):
    if not STOPLIGHT_TOKEN:
        logging.debug("No STOPLIGHT_TOKEN set, skipping Stoplight update.")
        return False
    # Implement Stoplight API call here if desired.
    logging.info("Would update Stoplight with %s (not implemented)", openapi_url)
    return True


# -------------------------
# Main
# -------------------------
def main(dry_run=False):
    logging.info("Start updater - dry_run=%s", dry_run)
    qayan, qtaj, audio_entries = build_quran_ayat_and_tajwid()

    safe_write_json(OUT_QAYAT, qayan)
    safe_write_json(OUT_TAJWID, qtaj)
    safe_write_json(OUT_AUDIO_PER_AYAT, audio_entries)

    # Git commit & push
    if not dry_run:
        # try local git first
        success = git_commit_and_push([OUT_QAYAT, OUT_TAJWID, OUT_AUDIO_PER_AYAT])
        if not success and GITHUB_TOKEN and GIT_REMOTE:
            # fallback: upload each file through GitHub API (repo name must be deduced from GIT_REMOTE)
            logging.info("Attempting GitHub API upload fallback")
            # extract repo full name from remote url if possible
            # supports: https://github.com/user/repo.git or git@github.com:user/repo.git
            repo_full = None
            if GIT_REMOTE.startswith("https://"):
                parts = GIT_REMOTE.rstrip(".git").split("/")
                repo_full = "/".join(parts[-2:])
            elif GIT_REMOTE.startswith("git@"):
                repo_full = GIT_REMOTE.split(":")[-1].rstrip(".git")
            if repo_full:
                upload_file_to_github_api(OUT_QAYAT, repo_full)
                upload_file_to_github_api(OUT_TAJWID, repo_full)
                upload_file_to_github_api(OUT_AUDIO_PER_AYAT, repo_full)
            else:
                logging.error("Could not determine repo_full_name from GIT_REMOTE: %s", GIT_REMOTE)

    logging.info("Updater finished.")


if __name__ == "__main__":
    # if you want to run regularly, call this script from cron/termux:tasker/etc.
    dry = "--dry-run" in sys.argv
    main(dry_run=dry)

