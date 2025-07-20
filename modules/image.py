import os
import requests
from telethon import events
from config import OWNER_ID, GOOGLE_API_KEY, CSE_ID

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# ====== Decorator to restrict commands to owner only ======
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    # --------------------
    # Google Image Search
    # --------------------
    @client.on(events.NewMessage(pattern=r"^\.img (.+)"))
    @is_owner
    async def google_image_search(event):
        query = event.pattern_match.group(1)
        await event.edit(f"🔍 **Searching for:** `{query}`")
        try:
            params = {
                "q": query,
                "cx": CSE_ID,
                "key": GOOGLE_API_KEY,
                "searchType": "image",
                "num": 5
            }
            response = requests.get(GOOGLE_SEARCH_URL, params=params).json()
            if "items" not in response:
                await event.edit("❌ No images found or API error.")
                return
            
            result_links = [item["link"] for item in response["items"]]
            await client.send_file(event.chat_id, result_links, caption=f"**Results for:** `{query}`")
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # ------------------------
    # Reverse Image Search
    # ------------------------
    @client.on(events.NewMessage(pattern=r"^\.reverse$"))
    @is_owner
    async def reverse_image_search(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to an image to reverse search.")
        
        reply = await event.get_reply_message()
        if not reply.media:
            return await event.reply("❌ No image found in the replied message.")
        
        img_path = await client.download_media(reply, "reverse_search.jpg")
        await event.edit("🔄 **Performing reverse image search...**")
        
        try:
            search_url = "http://www.google.com/searchbyimage/upload"
            multipart = {"encoded_image": (img_path, open(img_path, "rb")), "image_content": ""}
            response = requests.post(search_url, files=multipart, allow_redirects=False)
            fetch_url = response.headers.get("Location")

            if fetch_url:
                await event.edit(f"🔍 **Google Lens Result:** [Click Here]({fetch_url})")
            else:
                await event.edit("❌ Could not retrieve reverse search results.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
        finally:
            if os.path.exists(img_path):
                os.remove(img_path)
