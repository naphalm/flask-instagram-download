from flask import Flask, request, jsonify, send_file
import sys
import os
import threading
from utils import adapter

# Add the path to the downloader script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

REEL_REGEX = re.compile(r"instagram\.com/reel/([^/?]+)/?")

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload size 16MB

# GET endpoint for basic health check
@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server is running!"

# GET endpoint with simple JSON response
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "name": "InstaDownloader",
        "version": "1.0",
        "status": "running"
    })

  
@app.route('/download_reel', methods=['GET'])
def download_reel():
    message = adapter.download_reel()
    return jsonify(message)

 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)