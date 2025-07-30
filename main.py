from flask import Flask, request, jsonify
import subprocess
import uuid
import os

app = Flask(__name__)

AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route("/extract", methods=["POST"])
def extract_audio():
    data = request.get_json()
    video_url = data.get("url")
    if not video_url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    try:
        subprocess.run([
            "yt-dlp", "-x", "--audio-format", "mp3", "-o", filepath, video_url
        ], check=True)

        audio_url = request.host_url + f"static/audio/{filename}"
        return jsonify({"audio_url": audio_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🔽 ESTA PARTE ES CRUCIAL PARA QUE FLASK FUNCIONE EN RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
