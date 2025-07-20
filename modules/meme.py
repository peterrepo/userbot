import json
import os
import random
from telethon import events
from config import OWNER_ID

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
MEMES_FILE = os.path.join(DATA_DIR, "memes.json")

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.meme$"))
    @is_owner
    async def send_meme(event):
        try:
            with open(MEMES_FILE, "r", encoding="utf-8") as f:
                memes = json.load(f)
            
            if not memes:
                return await event.edit("❌ Meme list is empty.")
            
            meme = random.choice(memes)
            caption = meme.get("caption", "")
            url = meme.get("url", "")

            if url:
                await client.send_file(event.chat_id, url, caption=caption)
                await event.delete()
            else:
                await event.edit("❌ No URL found for this meme.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
