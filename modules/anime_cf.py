import asyncio
import aiohttp
from telethon import events
from config import OWNER_ID

# API endpoints
ANIME_QUOTE_API = "https://animechan.xyz/api/random"
ANIME_FACT_API = "https://anime-facts-rest-api.herokuapp.com/api/v1"
ANIME_CHARACTER_API = "https://api.jikan.moe/v4/characters?q="


def register(client):
    # ======================
    # Fetch JSON from URL
    # ======================
    async def fetch_json(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None

    # ======================
    # Random Anime Quote
    # ======================
    @client.on(events.NewMessage(pattern=r"\.animequote"))
    async def anime_quote(event):
        if event.sender_id != OWNER_ID:
            return
        await event.edit("`Fetching an anime quote...`")
        data = await fetch_json(ANIME_QUOTE_API)
        if data:
            quote = f"**{data['character']}** from *{data['anime']}*:\n\n`{data['quote']}`"
            await event.edit(quote)
        else:
            await event.edit("`Failed to fetch anime quote.`")

    # ======================
    # Random Anime Fact
    # ======================
    @client.on(events.NewMessage(pattern=r"\.animefact"))
    async def anime_fact(event):
        if event.sender_id != OWNER_ID:
            return
        await event.edit("`Fetching a random anime fact...`")
        data = await fetch_json(ANIME_FACT_API)
        if data and 'data' in data:
            facts = data.get('data', [])
            if facts:
                fact = facts[0].get('fact', "No fact found.")
                await event.edit(f"**Anime Fact:** `{fact}`")
            else:
                await event.edit("`No anime facts found.`")
        else:
            await event.edit("`Failed to fetch anime fact.`")

    # ======================
    # Anime Character Search
    # ======================
    @client.on(events.NewMessage(pattern=r"\.animechar (.+)"))
    async def anime_character(event):
        if event.sender_id != OWNER_ID:
            return
        query = event.pattern_match.group(1)
        await event.edit(f"`Searching for character '{query}'...`")
        data = await fetch_json(ANIME_CHARACTER_API + query)
        if data and 'data' in data and len(data['data']) > 0:
            char = data['data'][0]
            name = char.get('name', 'Unknown')
            about = char.get('about', 'No description available.')
            url = char.get('url', '')
            response = f"**Name:** {name}\n**More Info:** {url}\n\n{about[:400]}..."
            await event.edit(response)
        else:
            await event.edit(f"`Character '{query}' not found.`")
