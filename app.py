from flask import Flask, request, jsonify, send_file
from moviepy.video.VideoClip import TextClip, ColorClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_TOKEN = os.getenv("API_TOKEN", "super_secret_token_here")

@app.route('/generate', methods=['POST'])
def generate_video():
    token = request.headers.get("X-API-Token")
    if token != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    text = request.form.get("text")
    if not text:
        return jsonify({"error": "text is required"}), 400

    # Buat clip teks dengan durasi 5 detik
    clip_text = TextClip(text, fontsize=40, color='white', font='DejaVu-Sans')
    clip_text = clip_text.set_duration(5)

    # Buat background hitam sesuai ukuran teks
    background = ColorClip(size=clip_text.size, color=(0, 0, 0), duration=5)

    # Gabungkan background dan teks
    video = CompositeVideoClip([background, clip_text.set_pos('center')])

    filename = f"video_{uuid.uuid4().hex}.mp4"
    video.write_videofile(filename, fps=24, codec='libx264')

    response = send_file(filename, mimetype='video/mp4', as_attachment=True)

    @response.call_on_close
    def cleanup():
        if os.path.exists(filename):
            os.remove(filename)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

