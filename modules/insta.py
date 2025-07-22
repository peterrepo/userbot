import os
import requests
from telethon import events
from instagrapi import Client
from config import OWNER_ID

# ============================
# Instagram Client Login
# ============================
USERNAME = "serenehashira"
PASSWORD = "tomioka2008"

cl = Client()
try:
    cl.login(USERNAME, PASSWORD)
except Exception as e:
    print(f"❌ Instagram login failed: {e}")

# Ensure temp directory exists
TEMP_DIR = "insta_temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# ============================
# Register Function
# ============================
def register(client):

    # ----------------------------
    # USER INFO
    # ----------------------------
    @client.on(events.NewMessage(pattern=r"^\.instauser (.+)"))
    async def insta_user(event):
        if event.sender_id != OWNER_ID:
            return
        username = event.pattern_match.group(1)
        await event.respond(f"🔍 Fetching Instagram info for {username}...")

        try:
            user_info = cl.user_info_by_username(username).dict()
            bio = user_info.get("biography", "N/A")
            followers = user_info.get("follower_count", 0)
            following = user_info.get("following_count", 0)
            posts = user_info.get("media_count", 0)
            profile_pic_url = user_info.get("profile_pic_url_hd", user_info.get("profile_pic_url"))

            caption = (
                f"**📸 Instagram User Info**\n\n"
                f"**Username:** `{username}`\n"
                f"**Full Name:** {user_info.get('full_name', 'N/A')}\n"
                f"**Bio:** {bio}\n"
                f"**Followers:** {followers}\n"
                f"**Following:** {following}\n"
                f"**Posts:** {posts}"
            )

            if profile_pic_url:
                img_path = os.path.join(TEMP_DIR, "profile.jpg")
                try:
                    r = requests.get(profile_pic_url, timeout=10)
                    with open(img_path, "wb") as f:
                        f.write(r.content)
                    await event.respond(caption, file=img_path)
                    os.remove(img_path)
                except Exception as img_err:
                    await event.respond(f"{caption}\n\n⚠️ Failed to fetch profile image: {img_err}")
            else:
                await event.respond(caption)

        except Exception as e:
            await event.respond(f"❌ Error fetching user info: {e}")

    # ----------------------------
    # REELS DOWNLOAD
    # ----------------------------
    @client.on(events.NewMessage(pattern=r"^\.instareel (.+)"))
    async def insta_reel(event):
        if event.sender_id != OWNER_ID:
            return
        url = event.pattern_match.group(1)
        await event.respond("📥 Downloading reel...")
        try:
            media = cl.media_pk_from_url(url)
            file_path = cl.video_download(media, folder=TEMP_DIR)
            await event.respond("✅ Reel downloaded:", file=file_path)
            os.remove(file_path)
        except Exception as e:
            await event.respond(f"❌ Error downloading reel: {e}")

    # ----------------------------
    # POSTS DOWNLOAD
    # ----------------------------
    @client.on(events.NewMessage(pattern=r"^\.instapost (.+)"))
    async def insta_post(event):
        if event.sender_id != OWNER_ID:
            return
        url = event.pattern_match.group(1)
        await event.respond("📥 Downloading post...")
        try:
            media_pk = cl.media_pk_from_url(url)
            media_info = cl.media_info(media_pk).dict()
            if media_info.get("media_type") == 1:  # Photo
                file_path = cl.photo_download(media_pk, folder=TEMP_DIR)
            else:  # Video
                file_path = cl.video_download(media_pk, folder=TEMP_DIR)
            await event.respond("✅ Post downloaded:", file=file_path)
            os.remove(file_path)
        except Exception as e:
            await event.respond(f"❌ Error downloading post: {e}")

    # ----------------------------
    # STORIES DOWNLOAD
    # ----------------------------
    @client.on(events.NewMessage(pattern=r"^\.instastory (.+)"))
    async def insta_story(event):
        if event.sender_id != OWNER_ID:
            return
        username = event.pattern_match.group(1)
        await event.respond(f"📥 Fetching stories for {username}...")
        try:
            user_id = cl.user_id_from_username(username)
            stories = cl.user_stories(user_id)
            if not stories:
                await event.respond("⚠️ No active stories found.")
                return

            for story in stories:
                media_type = story.dict().get("media_type")
                if media_type == 1:  # Photo
                    file_path = cl.photo_download_by_url(story.dict()["thumbnail_url"], TEMP_DIR)
                else:  # Video
                    file_path = cl.video_download_by_url(story.dict()["video_url"], TEMP_DIR)
                await event.respond(file=file_path)
                os.remove(file_path)
        except Exception as e:
            await event.respond(f"❌ Error downloading story: {e}")
