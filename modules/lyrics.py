import requests
from telethon import events
from config import OWNER_ID

LYRICS_API_URL = "https://cse.google.com/cse.js?cx=07ff5954378d54935"  # Replace with real API endpoint

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.lyrics (.+)"))
    @is_owner
    async def lyrics_search(event):
        song = event.pattern_match.group(1)
        await event.edit(f"🔍 Searching lyrics for: **{song}**")
        try:
            params = {"q": song}
            res = requests.get(LYRICS_API_URL, params=params)
            res.raise_for_status()
            data = res.json()
            if not data or "lyrics" not in data:
                return await event.edit("❌ Lyrics not found.")

            lyrics = data["lyrics"]
            # Limit length for Telegram message
            if len(lyrics) > 4000:
                lyrics = lyrics[:4000] + "\n\n[Truncated]"

            await event.edit(f"**Lyrics for:** {song}\n\n{lyrics}")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

