import aiohttp
import re
from bs4 import BeautifulSoup
from telethon import events
from config import OWNER_ID

GENIUS_SEARCH_URL = "https://genius.com/api/search/multi?per_page=5&q="

# ---------------------
# Helper: Fetch lyrics
# ---------------------
async def fetch_lyrics(song_name: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            # Search on Genius
            async with session.get(GENIUS_SEARCH_URL + song_name) as resp:
                data = await resp.json()

            # Find the first song result
            sections = data.get("response", {}).get("sections", [])
            song_url = None
            for sec in sections:
                if sec["type"] == "song" and sec["hits"]:
                    song_url = sec["hits"][0]["result"]["url"]
                    break

            if not song_url:
                return "❌ No lyrics found."

            # Fetch lyrics page
            async with session.get(song_url) as resp:
                html = await resp.text()

            soup = BeautifulSoup(html, "html.parser")
            lyrics_div = soup.find("div", class_="lyrics")  # Old structure
            if not lyrics_div:
                # New structure: use data-lyrics-container
                lyrics_divs = soup.find_all("div", {"data-lyrics-container": "true"})
                lyrics_text = "\n".join([re.sub(r"<.*?>", "", str(x)) for x in lyrics_divs])
            else:
                lyrics_text = lyrics_div.get_text(separator="\n")

            lyrics_text = re.sub(r'\[.*?\]', '', lyrics_text).strip()
            if len(lyrics_text) > 4000:
                return lyrics_text[:4000] + "\n\n(…lyrics too long, truncated…)"

            return lyrics_text
    except Exception as e:
        return f"❌ Error fetching lyrics: {e}"

# ---------------------
# Telethon Command
# ---------------------
def register(client):
    @client.on(events.NewMessage(pattern=r"^\.lyrics (.+)"))
    async def lyrics_handler(event):
        if event.sender_id != OWNER_ID:
            return
        query = event.pattern_match.group(1)
        await event.respond(f"🔍 Searching lyrics for **{query}**…")
        lyrics = await fetch_lyrics(query)
        await event.respond(f"🎵 **Lyrics for {query}:**\n\n{lyrics}")
