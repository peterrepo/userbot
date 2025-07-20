import os
import requests
import json
from telethon import events
from config import OWNER_ID, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

# ====== Decorator for owner-only commands ======
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

# ====== Helper Function: Download Instagram Media via API ======
def download_instagram_post(url):
    try:
        api = f"https://api.vyro.ai/v1/ig?url={url}"  # Example third-party endpoint
        response = requests.get(api)
        if response.status_code != 200:
            return None
        data = response.json()
        return data.get("media", [])
    except Exception:
        return None

# ====== Module Register ======
def register(client):

    # ----------------------
    # Instagram Post Download
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.instadl (.+)"))
    @is_owner
    async def insta_download(event):
        url = event.pattern_match.group(1)
        await event.edit("⬇ **Downloading Instagram post...**")
        media_links = download_instagram_post(url)
        if not media_links:
            return await event.edit("❌ Failed to fetch media. Maybe it's private?")
        try:
            await client.send_file(event.chat_id, media_links, caption="**Instagram Post**")
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # ----------------------
    # Instagram User Info
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.instainfo (.+)"))
    @is_owner
    async def insta_info(event):
        username = event.pattern_match.group(1)
        await event.edit(f"🔍 **Fetching Instagram info for:** `{username}`")

        try:
            url = f"https://api.luxanna.cc/ig_user?username={username}"
            response = requests.get(url)
            if response.status_code != 200:
                return await event.edit("❌ Could not fetch user info.")

            data = response.json()
            info = (
                f"**Instagram Profile Info**\n\n"
                f"**Username:** {data.get('username')}\n"
                f"**Name:** {data.get('full_name')}\n"
                f"**Bio:** {data.get('biography')}\n"
                f"**Followers:** {data.get('followers')}\n"
                f"**Following:** {data.get('following')}\n"
                f"**Posts:** {data.get('posts')}\n"
                f"**Private:** {data.get('is_private')}\n"
            )
            profile_pic = data.get("profile_pic_url")
            if profile_pic:
                await client.send_file(event.chat_id, profile_pic, caption=info)
            else:
                await event.edit(info)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # ----------------------
    # Instagram Stories (Public)
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.instastory (.+)"))
    @is_owner
    async def insta_story(event):
        username = event.pattern_match.group(1)
        await event.edit(f"⬇ **Fetching latest stories for:** `{username}`")

        try:
            url = f"https://api.luxanna.cc/ig_stories?username={username}"
            response = requests.get(url)
            if response.status_code != 200:
                return await event.edit("❌ No stories found or user is private.")

            data = response.json().get("stories", [])
            if not data:
                return await event.edit("❌ No stories available.")

            await client.send_file(event.chat_id, data, caption=f"**Stories of {username}**")
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
