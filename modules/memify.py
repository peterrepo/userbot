import requests
from telethon import events
from config import OWNER_ID

IMGFLIP_API_URL = "https://api.imgflip.com/caption_image"
IMGFLIP_USERNAME = ""  # Set in config.py
IMGFLIP_PASSWORD = ""  # Set in config.py

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.memify (\d+) (.+)"))
    @is_owner
    async def create_meme(event):
        template_id = event.pattern_match.group(1)
        captions_text = event.pattern_match.group(2)
        captions = captions_text.split(";")

        await event.edit("🎬 Generating meme...")

        payload = {
            "template_id": template_id,
            "username": IMGFLIP_USERNAME,
            "password": IMGFLIP_PASSWORD,
            "boxes": [{"text": cap.strip()} for cap in captions]
        }

        try:
            response = requests.post(IMGFLIP_API_URL, json=payload).json()
            if response["success"]:
                meme_url = response["data"]["url"]
                await event.edit(f"🎉 Here is your meme:\n{meme_url}")
            else:
                await event.edit(f"❌ Error: {response['error_message']}")
        except Exception as e:
            await event.edit(f"❌ Exception: {e}")
