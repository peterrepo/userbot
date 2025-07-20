import asyncio
from telethon import events
from config import OWNER_ID

def register(client):
    @client.on(events.NewMessage(pattern=r"\.destruct"))
    async def destruct_cmd(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only command

        parts = event.raw_text.split(" ", 2)
        if len(parts) < 3:
            await event.reply("**Usage:** `.destruct <seconds> <message>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        try:
            delay = int(parts[1])
        except ValueError:
            await event.reply("**Error:** Invalid time format. Provide seconds as a number.")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        message = parts[2]
        sent_msg = await event.respond(f"💣 **Self-Destruct Message:** {message}")
        await asyncio.sleep(delay)
        await sent_msg.delete()
        await event.delete()
