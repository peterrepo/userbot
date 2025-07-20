import asyncio
from telethon import events
from config import OWNER_ID
from art import text2art

def register(client):
    @client.on(events.NewMessage(pattern=r"\.create"))
    async def create_cmd(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only

        # Get the text to stylize
        text = ""
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            text = reply_msg.text.strip() if reply_msg.text else ""
        else:
            parts = event.raw_text.split(" ", 1)
            if len(parts) > 1:
                text = parts[1].strip()

        if not text:
            await event.reply("**Usage:** `.create <text>` or reply to a message.")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        try:
            banner = text2art(text)
            # Send result in a code block
            await event.reply(f"```\n{banner}\n```")
        except Exception as e:
            await event.reply(f"**Error generating banner:** `{e}`")

        await asyncio.sleep(0.5)
        await event.delete()
