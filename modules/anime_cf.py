import aiohttp
from telethon import events
from config import OWNER_ID

API_URL = "https://graphql.anilist.co"
WAIFU_API = "https://api.waifu.pics/sfw/waifu"

# GraphQL queries
ANIME_QUERY = """
query ($search: String) {
  Media(search: $search, type: ANIME) {
    title { romaji english }
    description(asHtml: false)
    episodes status averageScore genres siteUrl
    coverImage { extraLarge }
  }
}
"""

MANGA_QUERY = """
query ($search: String) {
  Media(search: $search, type: MANGA) {
    title { romaji english }
    description(asHtml: false)
    chapters volumes status averageScore siteUrl
    coverImage { extraLarge }
  }
}
"""

CHARACTER_QUERY = """
query ($search: String) {
  Character(search: $search) {
    name { full native }
    description(asHtml: false)
    image { large }
    siteUrl
  }
}
"""

async def fetch_graphql(query, variables):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={"query": query, "variables": variables}) as r:
            return await r.json()

async def fetch_waifu():
    async with aiohttp.ClientSession() as session:
        async with session.get(WAIFU_API) as r:
            return await r.json()

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.anime\s+(.+)"))
    async def anime_cmd(event):
        if event.sender_id != OWNER_ID:
            return
        name = event.pattern_match.group(1).strip()
        msg = await event.respond(f"🔍 Searching for anime: {name}")
        data = await fetch_graphql(ANIME_QUERY, {"search": name})
        media = data.get("data", {}).get("Media")
        if not media:
            return await msg.edit("❌ No anime found with that title.")

        desc = (media.get("description") or "N/A").replace("<br>", "\n")[:500] + "..."
        caption = (
            f"**🎬 {media['title']['romaji']}**\n"
            f"English: {media['title'].get('english') or '—'}\n"
            f"Episodes: {media.get('episodes', '—')}\n"
            f"Status: {media.get('status','—')}\n"
            f"Score: {media.get('averageScore','—')}\n"
            f"Genres: {', '.join(media.get('genres',[])) or '—'}\n\n"
            f"{desc}\n\n[More info]({media['siteUrl']})"
        )
        await client.send_file(event.chat_id, media['coverImage']['extraLarge'], caption=caption, force_document=False)
        await msg.delete()

    @client.on(events.NewMessage(pattern=r"^\.manga\s+(.+)"))
    async def manga_cmd(event):
        if event.sender_id != OWNER_ID:
            return
        name = event.pattern_match.group(1).strip()
        msg = await event.respond(f"🔍 Searching for manga: {name}")
        data = await fetch_graphql(MANGA_QUERY, {"search": name})
        media = data.get("data", {}).get("Media")
        if not media:
            return await msg.edit("❌ No manga found with that title.")

        desc = (media.get("description") or "N/A").replace("<br>", "\n")[:500] + "..."
        caption = (
            f"**📚 {media['title']['romaji']}**\n"
            f"English: {media['title'].get('english') or '—'}\n"
            f"Chapters: {media.get('chapters','—')}, Volumes: {media.get('volumes','—')}\n"
            f"Status: {media.get('status','—')}\n"
            f"Score: {media.get('averageScore','—')}\n\n"
            f"{desc}\n\n[More info]({media['siteUrl']})"
        )
        await client.send_file(event.chat_id, media['coverImage']['extraLarge'], caption=caption, force_document=False)
        await msg.delete()

    @client.on(events.NewMessage(pattern=r"^\.mangachapter\s+(.+)\s+(\d+)$"))
    async def manga_chapter_cmd(event):
        if event.sender_id != OWNER_ID:
            return
        name = event.pattern_match.group(1).strip()
        chap = event.pattern_match.group(2)
        text = (
            f"**Requested Manga:** {name}\n"
            f"**Requested Chapter:** {chap}\n\n"
            "⚠️ AniList API provides **total chapter count** but does NOT include per‑chapter summaries or titles."
        )
        await event.respond(text)

    @client.on(events.NewMessage(pattern=r"^\.character\s+(.+)"))
    async def character_cmd(event):
        if event.sender_id != OWNER_ID:
            return
        name = event.pattern_match.group(1).strip()
        msg = await event.respond(f"🔍 Searching for character: {name}")
        data = await fetch_graphql(CHARACTER_QUERY, {"search": name})
        char = data.get("data", {}).get("Character")
        if not char:
            return await msg.edit("❌ No character found with that name.")

        desc = (char.get("description") or "N/A").replace("<br>", "\n")[:500] + "..."
        caption = (
            f"**👤 {char['name']['full']}**\n"
            f"Native: {char['name'].get('native','—')}\n\n"
            f"{desc}\n\n[More info]({char['siteUrl']})"
        )
        await client.send_file(event.chat_id, char['image']['large'], caption=caption, force_document=False)
        await msg.delete()

    @client.on(events.NewMessage(pattern=r"^\.waifu$"))
    async def waifu_cmd(event):
        if event.sender_id != OWNER_ID:
            return
        msg = await event.respond("🎴 Fetching waifu image...")
        data = await fetch_waifu()
        url = data.get("url")
        if not url:
            return await msg.edit("❌ Could not fetch a waifu image.")
        await msg.delete()
        await event.respond(file=url, caption="✨ **Here's your waifu!**")
