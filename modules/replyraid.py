import os
import random
from telethon import events

# Path to raid lines file
RAID_LINES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raid_lines.txt")

# Keep state of active raids
active_raids = set()
raid_lines = []

# Load raid lines
def load_raid_lines():
    global raid_lines
    if os.path.exists(RAID_LINES_FILE):
        with open(RAID_LINES_FILE, "r", encoding="utf-8") as f:
            raid_lines = [line.strip() for line in f if line.strip()]
    else:
        raid_lines = ["🔥 Default raid line!", "⚡ Boom!"]

def register(client):
    load_raid_lines()

    @client.on(events.NewMessage(pattern=r"^\.replyraid (on|off)$"))
    async def toggle_replyraid(event):
        """Enable or disable reply raid on a user by replying to their message."""
        if not event.is_reply:
            await event.respond("⚠ **Reply to a user's message to start raid!**")
            return

        action = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id

        if action == "on":
            active_raids.add(user_id)
            await event.respond(f"🚀 **Reply Raid ON** for user `{user_id}`!")
        else:
            active_raids.discard(user_id)
            await event.respond(f"🛑 **Reply Raid OFF** for user `{user_id}`.")

    @client.on(events.NewMessage)
    async def handle_incoming(event):
        """Check if a user in active raid triggers a reply."""
        if not active_raids or not event.sender_id:
            return

        # Check if sender is in active raid
        if event.sender_id in active_raids:
            # Send random raid line
            if raid_lines:
                line = random.choice(raid_lines)
                try:
                    await event.reply(line)
                except Exception as e:
                    print(f"[ReplyRaid Error] {e}")

