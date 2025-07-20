import json
import os
import random
from telethon import events
from config import OWNER_ID

# Path to replyraid data
REPLYRAID_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "replyraid.json")

# Active user ID for reply raid
active_reply_raid_user = None

# Load reply raid lines
def load_reply_lines():
    if not os.path.exists(REPLYRAID_FILE):
        return ["🔥 Default reply raid line! 🔥"]
    with open(REPLYRAID_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return ["🔥 Default reply raid line! 🔥"]

REPLY_LINES = load_reply_lines()

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    # -------------------
    # Start Reply Raid
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.replyraid$"))
    @is_owner
    async def start_reply_raid(event):
        global active_reply_raid_user
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a user's message to start reply raid.")
        active_reply_raid_user = reply.sender_id
        await event.edit(f"🔥 **Reply raid started on user ID:** `{active_reply_raid_user}`")

    # -------------------
    # Stop Reply Raid
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.stopreplyraid$"))
    @is_owner
    async def stop_reply_raid(event):
        global active_reply_raid_user
        active_reply_raid_user = None
        await event.edit("🛑 **Reply raid stopped.**")

    # -------------------
    # Reply Raid Trigger
    # -------------------
    @client.on(events.NewMessage)
    async def reply_raid_trigger(event):
        global active_reply_raid_user
        if not active_reply_raid_user:
            return

        # Check if this user triggered the raid
        if event.sender_id != active_reply_raid_user:
            return

        # Avoid self-replies
        if event.sender_id == OWNER_ID:
            return

        # Send a random raid line
        line = random.choice(REPLY_LINES)
        try:
            await event.reply(line)
        except Exception as e:
            print(f"[ReplyRaid Error] {e}")

