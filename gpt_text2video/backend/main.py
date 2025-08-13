from flask import Flask, request, jsonify, send_file
import os
from text2video import generate_script, create_video_from_text

app = Flask(__name__)

@app.route("/generate-script", methods=["POST"])
def generate_script_endpoint():
    data = request.get_json() or {{}}
    prompt = data.get("prompt") or ""
    if not prompt:
        return jsonify({{"error": "missing prompt"}}), 400
    script = generate_script(prompt)
    return jsonify({{"script": script}})

@app.route("/generate-video", methods=["POST"])
def generate_video_endpoint():
    data = request.get_json() or {{}}
    text = data.get("text") or ""
    if not text:
        return jsonify({{"error": "missing text"}}), 400
    out = create_video_from_text(text, output="output.mp4")
    return send_file(out, mimetype="video/mp4", as_attachment=True)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
