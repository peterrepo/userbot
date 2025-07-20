import time
from telethon import events
from config import OWNER_ID

start_time = time.time()

# Helper to get uptime
def get_uptime():
    now = time.time()
    uptime = int(now - start_time)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.ping$"))
    @is_owner
    async def ping_command(event):
        start = time.time()
        msg = await event.reply("🏓 **Pong!**")
        end = time.time()
        latency = round((end - start) * 1000, 2)
        await msg.edit(f"🏓 **Pong!**\n**Latency:** {latency}ms\n**Uptime:** {get_uptime()}")
