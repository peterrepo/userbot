import requests
from telethon import events
from config import OWNER_ID

# Free screenshot API (thum.io)
SCREENSHOT_API = "https://image.thum.io/get/width/1280/crop/800/noanimate/"

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.ss (.+)"))
    @is_owner
    async def screenshot_website(event):
        url = event.pattern_match.group(1)
        await event.edit(f"📸 Taking screenshot of `{url}` ...")
        try:
            screenshot_url = SCREENSHOT_API + url
            response = requests.get(screenshot_url, stream=True)

            if response.status_code != 200:
                return await event.edit(f"❌ Failed to fetch screenshot for `{url}`.")

            file_path = "website_screenshot.png"
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            await client.send_file(event.chat_id, file_path, caption=f"🌐 Screenshot of `{url}`")
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
