import os
import json
import requests
from telethon import events
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired
from config import OWNER_ID

# ============================
# Paths and Directories
# ============================
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SESSION_FILE = os.path.join(DATA_DIR, "session.json")
TEMP_DIR = os.path.join(DATA_DIR, "insta_temp")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ============================
# Instagram Client
# ============================
cl = Client()

def save_session():
    """Save current session to session.json"""
    with open(SESSION_FILE, "w") as f:
        json.dump(cl.get_settings(), f)
    print("✅ Instagram session saved.")

def load_session():
    """Load session from session.json"""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            settings = json.load(f)
        cl.set_settings(settings)
        try:
            cl.get_timeline_feed()
            print("✅ Instagram session loaded.")
            return True
        except LoginRequired:
            print("⚠️ Session expired. Need to re-login.")
            return False
    return False

def login_interactive():
    """Interactive login with OTP if required."""
    username = input("Enter Instagram Username: ")
    password = input("Enter Instagram Password: ")
    try:
        cl.login(username, password)
        save_session()
    except ChallengeRequired:
        print("⚠️ Instagram requires OTP.")
        cl.challenge_code_handler = lambda _: input("Enter OTP sent by Instagram: ")
        cl.login(username, password)
        save_session()
    except Exception as e:
        print(f"❌ Instagram login failed: {e}")
        raise

if not load_session():
    login_interactive()

# ============================
# Helper to Download File
# ============================
def download_url(url, filename):
    path = os.path.join(TEMP_DIR, filename)
    r = requests.get(url, timeout=15)
    with open(path, "wb") as f:
        f.write(r.content)
    return path

# ============================
# Register Bot Commands
# ============================
def register(client):

    # ----------------------------
    # USER INFO
    # ----------------------------
    @client.on(events.NewMessage(pattern=r"^\.instauser (.+)"))
    async def insta_user(event):
        if event.sender_id != OWNER_ID:
            return
        username = event.pattern_match.group(1).strip()
        await event.respond(f"🔍 Fetching Instagram info for {username}...")

        try:
            user_info = cl.user_info_by_username(username).dict()
            bio = user_info.get("biography", "N/A")
            followers = user_info.get("follower_count", 0)
            following = user_info.get("following_count", 0)
            posts = user_info.get("media_count", 0)
            profile_pic_url = user_info.get("profile_pic_url_hd") or user_info.get("profile_pic_url")

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
                img_path = download_url(profile_pic_url, "profile.jpg")
                await event.respond(caption, file=img_path)
                os.remove(img_path)
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
        url = event.pattern_match.group(1).strip()
        await event.respond("📥 Downloading reel...")
        try:
            media_pk = cl.media_pk_from_url(url)
            file_path = cl.video_download(media_pk, folder=TEMP_DIR)
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
        url = event.pattern_match.group(1).strip()
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
        username = event.pattern_match.group(1).strip()
        await event.respond(f"📥 Fetching stories for {username}...")
        try:
            user_id = cl.user_id_from_username(username)
            stories = cl.user_stories(user_id)
            if not stories:
                await event.respond("⚠️ No active stories found.")
                return

            for story in stories:
                s = story.dict()
                if s.get("media_type") == 1:
                    file_path = download_url(s["thumbnail_url"], "story.jpg")
                else:
                    file_path = download_url(s["video_url"], "story.mp4")
                await event.respond(file=file_path)
                os.remove(file_path)
        except Exception as e:
            await event.respond(f"❌ Error downloading story: {e}")
