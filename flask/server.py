from flask import Flask, request, jsonify, send_from_directory, abort
import yt_dlp
import os
import re
import sys

# Add the path to the downloader script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import adapter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size 16MB

DOWNLOAD_DIR = "downloads"
COOKIES_FILE = "cookies.txt"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

REEL_REGEX = re.compile(r"instagram\.com/reel/([^/?]+)/?")


def extract_reel_id(url: str) -> str | None:
    match = REEL_REGEX.search(url)
    return match.group(1) if match else None


@app.route("/download_reel", methods=["GET"])
def download_reel():
    reel_url = request.args.get("url")

    if not reel_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    reel_id = extract_reel_id(reel_url)
    if not reel_id:
        return jsonify({"error": "Invalid Instagram reel URL"}), 400

    filename = f"{reel_id}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    if not os.path.exists(filepath):
        ydl_opts = {
            "format": "mp4",
            "outtmpl": filepath,
            "merge_output_format": "mp4",
            "quiet": True,
            "noplaylist": True,
            "cookiefile": COOKIES_FILE,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([reel_url])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    public_url = request.host_url.rstrip("/") + f"/reels/{filename}"

    return jsonify({
        "reel_id": reel_id,
        "file_url": public_url
    })


@app.route("/reels/<path:filename>", methods=["GET"])
def serve_reel(filename):
    if not filename.endswith(".mp4"):
        abort(404)
    return send_from_directory(DOWNLOAD_DIR, filename, mimetype="video/mp4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
