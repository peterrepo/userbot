import requests
from telethon import events
from config import OWNER_ID  # Import OWNER_ID from your config.py

# ==============================
# CONFIG (Your API key and CSE ID)
# ==============================
GOOGLE_API_KEY = "AIzaSyBfFaDrZl0WYfPIisV9p05p_voCjw8oa4o"
GOOGLE_CSE_ID = "27648cc769b164f0a"

# ==============================
# Register module
# ==============================
def register(client):

    @client.on(events.NewMessage(pattern=r"^\.img (.+)"))
    async def google_image_search(event):
        # Owner-only check
        if event.sender_id != OWNER_ID:
            return

        query = event.pattern_match.group(1)
        await event.respond(f"🔍 Searching images for: `{query}`")

        try:
            url = (
                f"https://www.googleapis.com/customsearch/v1?"
                f"key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}&searchType=image&q={query}&num=5"
            )
            response = requests.get(url)

            if response.status_code != 200:
                await event.respond(f"❌ Google API Error: {response.status_code} - {response.text}")
                return

            data = response.json()

            if "items" not in data:
                await event.respond("❌ **No image results found.**")
                return

            # Get top 5 image URLs
            image_links = [item["link"] for item in data["items"][:5]]

            # Send images
            for link in image_links:
                try:
                    await event.client.send_file(event.chat_id, link)
                except Exception as e:
                    await event.respond(f"⚠️ Skipped broken image link. Error: `{e}`")

        except Exception as e:
            await event.respond(f"❌ Error while fetching images: `{e}`")
