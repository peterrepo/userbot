import os
import yt_dlp
import requests
from telethon import events
from config import OWNER_ID, YT_API_KEY

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def youtube_search(query, max_results=5):
    """Search YouTube using YouTube Data API."""
    params = {
        "part": "snippet",
        "q": query,
        "key": YT_API_KEY,
        "maxResults": max_results,
        "type": "video",
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data["items"]:
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            url = f"https://www.youtube.com/watch?v={video_id}"
            results.append(f"🎬 **{title}**\n{url}")
        return "\n\n".join(results)
    return None


def register(client):

    # -------------------
    # YouTube Search
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.yt (.+)"))
    @is_owner
    async def yt_search(event):
        query = event.pattern_match.group(1).strip()
        await event.edit(f"🔍 **Searching YouTube for:** `{query}`")

        if not YT_API_KEY:
            return await event.edit("❌ YouTube API Key not set in `config.py`.")

        try:
            results = youtube_search(query)
            if not results:
                return await event.edit("❌ No results found.")
            await event.edit(results)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # YouTube Downloader (Audio/Video)
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.ytdl (.+)"))
    @is_owner
    async def yt_download(event):
        url = event.pattern_match.group(1).strip()
        await event.edit("📥 **Downloading video from YouTube...**")

        try:
            ydl_opts = {
                "format": "best",
                "outtmpl": "downloads/%(title)s.%(ext)s",
                "quiet": True,
            }
            os.makedirs("downloads", exist_ok=True)
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)

            await event.edit("📤 **Uploading video...**")
            await client.send_file(event.chat_id, file_path, caption=f"🎬 {info.get('title')}")
            os.remove(file_path)
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Download failed: {e}")
