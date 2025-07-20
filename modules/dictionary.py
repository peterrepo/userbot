import asyncio
import aiohttp
from telethon import events
from config import OWNER_ID

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def register(client):
    @client.on(events.NewMessage(pattern=r"\.dict"))
    async def dict_cmd(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only command

        parts = event.raw_text.split(" ", 1)
        if len(parts) < 2:
            await event.reply("**Usage:** `.dict <word>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        word = parts[1].strip()
        await event.reply(f"🔍 **Searching meaning for:** `{word}`")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL + word) as response:
                    if response.status == 200:
                        data = await response.json()
                        if isinstance(data, list) and data:
                            meaning = data[0].get("meanings", [{}])[0]
                            definition = meaning.get("definitions", [{}])[0].get("definition", "No definition found.")
                            part_of_speech = meaning.get("partOfSpeech", "unknown")
                            reply = f"**Word:** `{word}`\n**Part of Speech:** {part_of_speech}\n**Definition:** {definition}"
                        else:
                            reply = f"⚠ No results found for `{word}`."
                    else:
                        reply = f"⚠ API Error: {response.status}"
        except Exception as e:
            reply = f"❌ **Error:** {e}"

        await event.respond(reply)
        await asyncio.sleep(0.5)
        await event.delete()
