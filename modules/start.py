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

    @client.on(events.NewMessage(pattern=r"^\.start$"))
    @is_owner
    async def start_cmd(event):
        await event.edit(
            "✅ **Ultimate Userbot is Running!**\n\n"
            "Use `.help` or check modules for available commands."
        )
