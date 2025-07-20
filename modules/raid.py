import asyncio
import random
import os
from telethon import events
from config import OWNER_ID

# Path to raid lines file
RAID_LINES_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "raid_lines.txt")

# Load raid lines
def load_raid_lines():
    if not os.path.exists(RAID_LINES_FILE):
        return ["🔥 Default raid line! 🔥"]
    with open(RAID_LINES_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines or ["🔥 Default raid line! 🔥"]

RAID_LINES = load_raid_lines()
active_raid = False  # Flag to control raid state

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
    # Start Raid
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.raid (\d+)$"))
    @is_owner
    async def start_raid(event):
        global active_raid
        count = int(event.pattern_match.group(1))
        active_raid = True
        await event.edit(f"⚠️ Starting raid with {count} messages... Use `.stopraid` to stop early.")

        try:
            for i in range(count):
                if not active_raid:
                    await client.send_message(event.chat_id, "🛑 Raid stopped.")
                    break
                line = random.choice(RAID_LINES)
                await client.send_message(event.chat_id, line)
                await asyncio.sleep(0.4)  # Delay between messages
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Stop Raid
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.stopraid$"))
    @is_owner
    async def stop_raid(event):
        global active_raid
        if not active_raid:
            return await event.edit("❌ No active raid to stop.")
        active_raid = False
        await event.edit("🛑 **Raid has been stopped.**")

    # -------------------
    # Add Raid Line
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.addrline (.+)"))
    @is_owner
    async def add_raid_line(event):
        new_line = event.pattern_match.group(1)
        try:
            with open(RAID_LINES_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n{new_line}")
            RAID_LINES.append(new_line)
            await event.edit(f"✅ Added new raid line:\n`{new_line}`")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Show Random Raid Line
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.rline$"))
    @is_owner
    async def show_random_line(event):
        line = random.choice(RAID_LINES)
        await event.edit(f"🎯 Random Raid Line:\n`{line}`")
