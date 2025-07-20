import asyncio
import time
from telethon import events
from config import OWNER_ID

START_TIME = time.time()


def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    return ":".join(reversed(time_list))


def register(client):
    # ======================
    # Ping Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.ping$"))
    async def ping(event):
        if event.sender_id != OWNER_ID:
            return
        start = time.time()
        msg = await event.reply("Pong!")
        end = time.time()
        await msg.edit(f"**Pong!** `{round((end - start) * 1000)} ms`")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Alive Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.alive$"))
    async def alive(event):
        if event.sender_id != OWNER_ID:
            return
        await event.reply("**I am alive and running!**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Uptime Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.uptime$"))
    async def uptime(event):
        if event.sender_id != OWNER_ID:
            return
        uptime_str = get_readable_time(time.time() - START_TIME)
        await event.reply(f"**Uptime:** `{uptime_str}`")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # WhoAmI Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.whoami$"))
    async def whoami(event):
        if event.sender_id != OWNER_ID:
            return
        user = await event.get_sender()
        await event.reply(f"**Your Name:** {user.first_name}\n**User ID:** {user.id}")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Help Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.help$"))
    async def help_cmd(event):
        if event.sender_id != OWNER_ID:
            return
        commands = """
**Available Commands:**
- `.ping` - Check response time.
- `.alive` - Check if bot is alive.
- `.uptime` - Get uptime of the bot.
- `.whoami` - Get your name and ID.
- `.help` - Show this help message.
"""
        await event.reply(commands)
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Message Count (DM + Groups)
    # ======================
    @client.on(events.NewMessage(pattern=r"\.messagecount$"))
    async def message_count(event):
        if event.sender_id != OWNER_ID:
            return
        async for dialog in client.iter_dialogs():
            messages = await client.get_messages(dialog.id, limit=1)
        await event.reply("**Message count command is under development.**")
        await asyncio.sleep(0.5)
        await event.delete()
