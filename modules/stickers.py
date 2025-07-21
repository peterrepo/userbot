# modules/stickers.py
import asyncio
from telethon import events
from telethon.tl.types import InputMessagesFilterPhotos
from config import OWNER_ID

def register(client):
    @client.on(events.NewMessage(pattern=r"^\.sticker$"))
    async def create_sticker(event):
        if event.sender_id != OWNER_ID:
            return
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            await event.respond("⚠️ Reply to an image or sticker to convert.")
            return
        await event.respond("🖼 Converting to sticker... (simulation)")
        # You can add Pillow or telegraph code to make sticker

    @client.on(events.NewMessage(pattern=r"^\.stickerinfo$"))
    async def sticker_info(event):
        if event.sender_id != OWNER_ID:
            return
        await event.respond("ℹ Sticker info (simulation).")

    @client.on(events.NewMessage(pattern=r"^\.stickersearch (.+)"))
    async def sticker_search(event):
        if event.sender_id != OWNER_ID:
            return
        query = event.pattern_match.group(1)
        await event.respond(f"🔍 Searching stickers for `{query}` (simulation).")

    print("✅ Stickers module loaded")
