import requests
from telethon import events
from config import OWNER_ID, BITLY_API_KEY

TINY_API = "https://tinyurl.com/api-create.php"

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def bitly_shorten(url):
    """Shorten URL using Bitly API if BITLY_API_KEY is set."""
    headers = {"Authorization": f"Bearer {BITLY_API_KEY}"}
    json_data = {"long_url": url}
    response = requests.post("https://api-ssl.bitly.com/v4/shorten", json=json_data, headers=headers)
    if response.status_code == 200:
        return response.json().get("link")
    else:
        return None


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.tiny (.+)"))
    @is_owner
    async def shorten_url(event):
        url = event.pattern_match.group(1).strip()
        await event.edit("🔗 **Shortening URL...**")

        try:
            if BITLY_API_KEY:
                short_url = bitly_shorten(url)
            else:
                short_url = requests.get(TINY_API, params={"url": url}).text

            if not short_url or "http" not in short_url:
                return await event.edit("❌ Failed to shorten the URL.")

            await event.edit(f"**Shortened URL:** {short_url}")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
