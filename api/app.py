from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/get_mp4", methods=["POST"])
def get_mp4():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "best[ext=mp4]/best",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict.get("url", None)
        return jsonify({"mp4_url": video_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
