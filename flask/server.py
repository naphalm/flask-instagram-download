from flask import Flask, request, jsonify, send_from_directory, abort

# gunicorn --workers 3 --bind 0.0.0.0:8000 server:app

# sudo systemctl restart gunicorn
# systemctl daemon-reexec
# systemctl daemon-reload
# systemctl enable gunicorn
# systemctl start gunicorn

# systemctl status gunicorn
# journalctl -u gunicorn --no-pager

# ps aux | grep gunicorn


# Add the path to the downloader script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import adapter
from utils import instagram

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size 16MB

@app.route("/download_reel", methods=["GET"])
def download_reel():
    input_url = request.args.get("url")
    if not input_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    reel_id = extract_reel_id(input_url)
    if not reel_id:
        return jsonify({"error": "Invalid Instagram URL"}), 400
    
    
    reel_id, public_url, metadata = instagram.download_reel(input_url)

    return jsonify({
        "reel_id": reel_id,
        "file_url": public_url,
        "metadata": metadata
    })


@app.route("/reels/<path:filename>", methods=["GET"])
def serve_reel(filename):
    if not filename.endswith(".mp4"):
        abort(404)
    return send_from_directory(instagram.DOWNLOAD_DIR, filename, mimetype="video/mp4")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
