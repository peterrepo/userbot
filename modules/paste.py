import requests
from telethon import events
from config import OWNER_ID

PASTE_API = "https://hastebin.com/documents"  # Default paste service

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def upload_to_hastebin(text):
    try:
        res = requests.post(PASTE_API, data=text.encode('utf-8'))
        res.raise_for_status()
        key = res.json().get("key")
        return f"https://hastebin.com/{key}"
    except Exception:
        return None

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.paste$"))
    @is_owner
    async def paste_command(event):
        reply = await event.get_reply_message()
        if not reply or not reply.text:
            return await event.edit("❌ Reply to some text to paste.")

        await event.edit("⏳ Uploading text to Hastebin...")
        link = upload_to_hastebin(reply.text)
        if link:
            await event.edit(f"✅ Pasted successfully: {link}")
        else:
            await event.edit("❌ Failed to upload text.")
