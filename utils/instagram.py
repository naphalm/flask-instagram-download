# instagram.py

import yt_dlp
import os
import re
import sys

DOWNLOAD_DIR = "/var/www/instagram-reels"
COOKIES_FILE = "cookies.txt"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

REEL_REGEX = re.compile(
    r"instagram\.com/(?:reel|reels|p)/([^/?]+)/?",
    re.IGNORECASE
)

def extract_reel_id(url: str) -> str | None:
    match = REEL_REGEX.search(url)
    return match.group(1) if match else None


def normalize_url(reel_id: str) -> str:
    # Always convert to /p/<ID>/ for yt-dlp
    return f"https://www.instagram.com/p/{reel_id}/"


def download_reel(url, host_url):
    if not url:
        return None, None, {"error": "Missing 'url' parameter"}

    reel_id = extract_reel_id(url)
    if not reel_id:
        return None, None, {"error": "Invalid Instagram URL"}

    normalized_url = normalize_url(reel_id)
    filename = f"{reel_id}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

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
            info = ydl.extract_info(normalized_url, download=False)
            if not os.path.exists(filepath):
                ydl.download([normalized_url])
    except Exception as e:
        return None, None, {"error": f"yt-dlp failed: {str(e)}"}

    metadata = {
        "id": info.get("id"),
        "title": info.get("title"),
        "description": info.get("description"),
        "uploader": info.get("uploader"),
        "upload_date": info.get("upload_date"),
        "tags": info.get("tags"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "webpage_url": info.get("webpage_url"),
        "thumbnail": info.get("thumbnail"),
    }

    public_url = host_url.rstrip("/") + f"/reels/{filename}"
    return reel_id, public_url, metadata