import os
import zipfile
import requests
import yt_dlp

DOWNLOAD_DIR = "/var/www/instagram-reels"

SC_BOT_TOKEN = os.getenv("SC_TELEGRAM_BOT_TOKEN")
# CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def ensure_download_dir():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def send_to_telegram(chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{SC_BOT_TOKEN}/sendDocument"

    with open(file_path, "rb") as f:
        requests.post(
            url,
            data={"chat_id": chat_id, "caption": caption},
            files={"document": f}
        )


def create_zip(file_paths, zip_name):

    zip_path = os.path.join(DOWNLOAD_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for file in file_paths:
            z.write(file, os.path.basename(file))

    return zip_path


def download_and_send(input_url, chat_id):

    ensure_download_dir()

    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(title)s.%(ext)s",

    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    }

    downloaded_files = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(input_url, download=True)

        # PLAYLIST
        if "entries" in info:

            for entry in info["entries"]:
                if entry is None:
                    continue

                filename = ydl.prepare_filename(entry)
                downloaded_files.append(filename)

            zip_name = f"{info.get('title','playlist')}.zip"
            zip_path = create_zip(downloaded_files, zip_name)

            send_to_telegram(zip_path, caption="SoundCloud playlist")

            return {
                "type": "playlist",
                "files": len(downloaded_files),
                "zip": zip_name
            }

        # SINGLE TRACK
        else:

            filename = ydl.prepare_filename(info)

            send_to_telegram(chat_id,filename, caption=info.get("title"))

            return {
                "type": "track",
                "file": os.path.basename(filename)
            }