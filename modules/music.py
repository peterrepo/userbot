import os
import requests
import youtube_dl
from telethon import events
from config import OWNER_ID, YT_API_KEY

# Temporary folder for downloads
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

# Search YouTube for a song
def youtube_search(query):
    try:
        search_url = f"https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "key": YT_API_KEY,
            "maxResults": 1
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        if "items" not in data or not data["items"]:
            return None
        video_id = data["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    except Exception:
        return None

def register(client):

    # ----------------------
    # Music Search
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.music (.+)"))
    @is_owner
    async def music_search(event):
        query = event.pattern_match.group(1)
        await event.edit(f"🎵 Searching music for: **{query}**")
        url = youtube_search(query)
        if not url:
            return await event.edit("❌ No music found.")
        await event.edit(f"🎧 Found track: {url}")

    # ----------------------
    # Music Download
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.song (.+)"))
    @is_owner
    async def music_download(event):
        query = event.pattern_match.group(1)
        await event.edit(f"⬇ Downloading song for: **{query}**")
        url = youtube_search(query)
        if not url:
            return await event.edit("❌ No song found.")

        file_path = os.path.join(DOWNLOAD_DIR, "song.mp3")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            await client.send_file(event.chat_id, file_path, caption=f"🎶 **{query}**")
            os.remove(file_path)
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
