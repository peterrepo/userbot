import os
import asyncio
import time
import yt_dlp
from telethon import events
from config import OWNER_ID

# ======================
# Paths and Directories
# ======================
MODULE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(MODULE_DIR, "../data")
DOWNLOAD_DIR = os.path.join(DATA_DIR, "music")
COOKIES_FILE = os.path.join(MODULE_DIR, "cookies.txt")

# Ensure all required directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# ======================
# Auto-Clean Old Files
# ======================
def clean_old_files(directory, max_age_hours=1):
    now = time.time()
    max_age = max_age_hours * 3600
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            if now - os.path.getmtime(file_path) > max_age:
                try:
                    os.remove(file_path)
                    print(f"🗑 Deleted old file: {file_path}")
                except Exception as e:
                    print(f"❌ Error deleting file {file_path}: {e}")


# ======================
# Download Music
# ======================
def download_song(query):
    """
    Downloads the best audio for the given query from YouTube.
    Returns (file_path, title).
    """
    clean_old_files(DOWNLOAD_DIR)  # Clean old files before download
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "cookiefile": COOKIES_FILE if os.path.isfile(COOKIES_FILE) else None,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        if not info or "entries" not in info or len(info["entries"]) == 0:
            raise Exception("No results found for this query.")
        entry = info["entries"][0]
        downloaded_file = ydl.prepare_filename(entry)
        mp3_file = os.path.splitext(downloaded_file)[0] + ".mp3"
        return mp3_file, entry.get("title", "Unknown Title")


# ======================
# Register Command
# ======================
def register(client):
    @client.on(events.NewMessage(pattern=r"^\.music (.+)"))
    async def music_handler(event):
        if event.sender_id != OWNER_ID:
            return

        query = event.pattern_match.group(1).strip()
        await event.respond(f"🎵 Searching and downloading: {query} ...")
        await asyncio.sleep(2)
        await event.delete()

        try:
            mp3_path, title = await asyncio.get_event_loop().run_in_executor(
                None, download_song, query
            )
            await event.client.send_file(event.chat_id, mp3_path, caption=f"🎶 {title}")
        except Exception as e:
            await event.respond(f"❌ Error: {e}")
