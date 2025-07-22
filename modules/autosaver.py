import os
from telethon import events
from telethon.tl.types import PeerUser
from config import OWNER_ID

# ==========================
# Paths & Setup
# ==========================
DATA_DIR = "data"
AUTOSAVER_FOLDER = os.path.join(DATA_DIR, "autosaver")
AUTOSAVER_STATE_FILE = os.path.join(DATA_DIR, "autosaver_state.txt")

os.makedirs(AUTOSAVER_FOLDER, exist_ok=True)
if not os.path.exists(AUTOSAVER_STATE_FILE):
    with open(AUTOSAVER_STATE_FILE, "w") as f:
        f.write("off")


# ==========================
# Helper Functions
# ==========================
def is_autosaver_on():
    try:
        with open(AUTOSAVER_STATE_FILE, "r") as f:
            return f.read().strip() == "on"
    except FileNotFoundError:
        return False


def set_autosaver_state(state: str):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(AUTOSAVER_STATE_FILE, "w") as f:
        f.write(state)


# ==========================
# Module Registration
# ==========================
def register(client):
    @client.on(events.NewMessage(pattern=r"^\.autosaveron$"))
    async def autosaver_on(event):
        if event.sender_id != OWNER_ID:
            return
        set_autosaver_state("on")
        await event.respond("✅ **AutoSaver Enabled. Saving all private chat media (including view-once).**")

    @client.on(events.NewMessage(pattern=r"^\.autosaveroff$"))
    async def autosaver_off(event):
        if event.sender_id != OWNER_ID:
            return
        set_autosaver_state("off")
        await event.respond("❌ **AutoSaver Disabled.**")

    @client.on(events.NewMessage(pattern=r"^\.autosaverstatus$"))
    async def autosaver_status(event):
        if event.sender_id != OWNER_ID:
            return
        state = "ON" if is_autosaver_on() else "OFF"
        await event.respond(f"**AutoSaver is currently:** `{state}`")

    @client.on(events.NewMessage(incoming=True))
    async def autosaver_handler(event):
        if not is_autosaver_on():
            return

        if not isinstance(event.peer_id, PeerUser):
            return

        if not event.media:
            return

        try:
            temp_file = os.path.join(AUTOSAVER_FOLDER, f"{event.id}")
            os.makedirs(AUTOSAVER_FOLDER, exist_ok=True)

            # Download media
            downloaded_path = await client.download_media(event.message, file=temp_file)

            if not downloaded_path or not os.path.exists(downloaded_path):
                print(f"❌ Failed to download media from {event.sender_id}")
                return

            # Forward to Saved Messages
            await client.send_file("me", downloaded_path, caption=f"📥 Auto-saved from **{event.sender_id}**")

            # Delete temp file
            try:
                os.remove(downloaded_path)
            except OSError:
                pass

            print(f"✅ Auto-saved media from {event.sender_id}")
        except Exception as e:
            print(f"❌ Error saving media: {e}")
