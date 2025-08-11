# app.py
import os, uuid, threading, json, time
from flask import Flask, request, jsonify, send_file, abort
from dotenv import load_dotenv
from video_worker import enqueue_job, JOBS_DIR, get_job_status

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN","changeme")

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    token = request.headers.get("X-API-Token") or request.form.get("api_token")
    if token != API_TOKEN:
        return jsonify({"error":"unauthorized"}), 401

    text = request.form.get("text") or request.json.get("text")
    keyword = request.form.get("keyword") or request.json.get("keyword")
    place = request.form.get("place") or request.json.get("place")

    if not text:
        return jsonify({"error":"text required"}), 400

    job_id = str(uuid.uuid4())
    enqueue_job(job_id, text, keyword, place)
    return jsonify({"job_id": job_id, "status_url": f"/status/{job_id}", "download_url": f"/download/{job_id}"}), 202

@app.route("/status/<job_id>", methods=["GET"])
def status(job_id):
    s = get_job_status(job_id)
    if not s:
        return jsonify({"error":"job not found"}), 404
    return jsonify(s)

@app.route("/download/<job_id>", methods=["GET"])
def download(job_id):
    jobdir = os.path.join(JOBS_DIR, job_id)
    mp = os.path.join(jobdir, "final.mp4")
    if os.path.exists(mp):
        return send_file(mp, as_attachment=True)
    else:
        return jsonify({"error":"not ready"}), 404

if __name__ == "__main__":
    os.makedirs(JOBS_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)

