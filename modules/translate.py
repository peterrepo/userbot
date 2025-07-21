import aiohttp
from telethon import events
from config import OWNER_ID

API_URL = "https://api.mymemory.translated.net/get"

async def translate_text(text, target_lang="en"):
    async with aiohttp.ClientSession() as session:
        params = {"q": text, "langpair": f"auto|{target_lang}"}
        async with session.get(API_URL, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["responseData"]["translatedText"]
            return "Translation failed."

def register(client):
    @client.on(events.NewMessage(pattern=r"^\.tr (.+)$"))
    async def translate_handler(event):
        if event.sender_id != OWNER_ID:
            return
        args = event.pattern_match.group(1).split(maxsplit=1)
        if len(args) == 2:
            lang, text = args
        else:
            lang = "en"
            text = args[0]
        await event.respond("🔄 Translating...")
        translated = await translate_text(text, lang)
        await event.respond(f"**Translated ({lang}):**\n`{translated}`")
