from flask import Flask, request, jsonify, send_file
import sys
import os
import threading

# Add the path to the downloader script to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the function from the correct location
# from download_youtube import download_youtube_video

from utils import adapter

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

  
@app.route('/download_reel', methods=['POST'])
def download_reel():
    adapter.download_reel()



# @app.route('/generate_video_from_voice', methods=['POST'])
# def generate_video_from_voice():
#     pass


# @app.route('/transcribe_audio', methods=['POST'])
# def transcribe_audio():
#     pass
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)