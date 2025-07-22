import os
import asyncio
import time
from datetime import datetime, timedelta
from telethon import events
from telethon.tl.types import MessageMediaDocument
import yt_dlp

from config import OWNER_ID

# Path for cookies
COOKIES_PATH = os.path.join(os.path.dirname(__file__), "cookies.txt")
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "../data/youtube_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Auto-clean downloaded files older than 1 hour
def clean_old_files():
    now = time.time()
    for filename in os.listdir(DOWNLOAD_DIR):
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        if os.path.isfile(file_path) and now - os.path.getmtime(file_path) > 3600:
            os.remove(file_path)

# Search YouTube using yt-dlp
def yt_search(query, limit=5):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
        "noplaylist": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None
    }
    results = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            for entry in info.get("entries", []):
                results.append({
                    "title": entry.get("title"),
                    "url": entry.get("url"),
                    "duration": entry.get("duration"),
                    "views": entry.get("view_count")
                })
    except Exception as e:
        return f"❌ Error searching YouTube: {e}"
    return results

# Download YouTube video using yt-dlp
def yt_download(url):
    clean_old_files()
    output_template = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
        "quiet": True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path
    except Exception as e:
        return f"❌ Error downloading video: {e}"

# Fetch channel info
def yt_channel_info(channel_url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            return {
                "title": info.get("title"),
                "description": info.get("description"),
                "subscribers": info.get("subscriber_count"),
                "url": info.get("webpage_url")
            }
    except Exception as e:
        return f"❌ Error fetching channel info: {e}"

# Register events
def register(client):

    @client.on(events.NewMessage(pattern=r"^\.yt (.+)"))
    async def yt_search_handler(event):
        if event.sender_id != OWNER_ID:
            return
        query = event.pattern_match.group(1)
        await event.respond(f"🔍 Searching YouTube for: {query} ...")
        results = yt_search(query)
        if isinstance(results, str):
            await event.respond(results)
        else:
            msg = "🎥 **Top YouTube Results:**\n\n"
            for idx, r in enumerate(results, 1):
                msg += f"{idx}. [{r['title']}]({r['url']}) - {r['duration']}s - {r['views']} views\n"
            await event.respond(msg, link_preview=False)

    @client.on(events.NewMessage(pattern=r"^\.ytdl (.+)"))
    async def yt_download_handler(event):
        if event.sender_id != OWNER_ID:
            return
        url = event.pattern_match.group(1)
        await event.respond(f"⬇️ Downloading video from: {url}")
        file_path = yt_download(url)
        if isinstance(file_path, str) and file_path.startswith("❌"):
            await event.respond(file_path)
        else:
            await event.respond("🎵 Uploading downloaded file...")
            await event.respond(file=file_path)
            clean_old_files()

    @client.on(events.NewMessage(pattern=r"^\.ytchannel (.+)"))
    async def yt_channel_handler(event):
        if event.sender_id != OWNER_ID:
            return
        channel_url = event.pattern_match.group(1)
        await event.respond(f"📡 Fetching channel info for: {channel_url}")
        info = yt_channel_info(channel_url)
        if isinstance(info, str):
            await event.respond(info)
        else:
            msg = (
                f"**Channel:** {info['title']}\n"
                f"**Subscribers:** {info['subscribers']}\n"
                f"**URL:** {info['url']}\n\n"
                f"**Description:** {info['description']}"
            )
            await event.respond(msg)
