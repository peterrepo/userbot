import os
import sys
from telethon import events
from config import OWNER_ID

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.restart$"))
    @is_owner
    async def restart_bot(event):
        await event.edit("🔄 **Restarting Userbot...**")
        try:
            # Restart the current Python process
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            await event.edit(f"❌ Restart failed: {e}")
