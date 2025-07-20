import aiohttp
import random
from telethon import events
from config import OWNER_ID, TENOR_API_KEY

# TENOR API base URL
TENOR_SEARCH_URL = "https://tenor.googleapis.com/v2/search"

def register(client):
    @client.on(events.NewMessage(pattern=r"\.gif (.+)"))
    async def send_gif(event):
        if event.sender_id != OWNER_ID:
            return
        
        query = event.pattern_match.group(1).strip()
        if not query:
            await event.respond("❌ **Please provide a search query.**")
            return

        await event.respond(f"🔎 **Searching GIFs for:** `{query}` ...")
        await event.delete()

        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    "q": query,
                    "key": TENOR_API_KEY,
                    "limit": 10
                }
                async with session.get(TENOR_SEARCH_URL, params=params) as response:
                    if response.status != 200:
                        await event.respond("❌ **Failed to fetch GIFs.**")
                        return
                    data = await response.json()
            
            # Extract GIFs from response
            if "results" not in data or len(data["results"]) == 0:
                await event.respond(f"❌ **No GIFs found for:** `{query}`")
                return

            gif_urls = [result["media_formats"]["gif"]["url"] for result in data["results"]]
            chosen_gif = random.choice(gif_urls)

            # Send the chosen GIF
            await client.send_file(event.chat_id, chosen_gif)

        except Exception as e:
            await event.respond(f"⚠ **Error:** {str(e)}")
