import os
import asyncio
from telethon import events
from config import OWNER_ID

# Directory for storing files
FILES_DIR = "data/files"

# Ensure directory exists
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

def register(client):

    # ========== UPLOAD A FILE ==========
    @client.on(events.NewMessage(pattern=r"\.upload (.+)"))
    async def upload_file(event):
        if event.sender_id != OWNER_ID:
            return
        file_path = event.pattern_match.group(1).strip()
        if not os.path.exists(file_path):
            await event.reply(f"❌ File `{file_path}` not found.")
        else:
            await event.reply("📤 **Uploading file...**")
            await event.reply(file=file_path)
        await asyncio.sleep(0.5)
        await event.delete()

    # ========== DOWNLOAD REPLIED FILE ==========
    @client.on(events.NewMessage(pattern=r"\.download"))
    async def download_file(event):
        if event.sender_id != OWNER_ID:
            return
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            await event.reply("❌ **Reply to a file to download.**")
        else:
            file_path = os.path.join(FILES_DIR, f"{reply.id}.file")
            await reply.download_media(file_path)
            await event.reply(f"✅ **File saved to:** `{file_path}`")
        await asyncio.sleep(0.5)
        await event.delete()

    # ========== LIST SAVED FILES ==========
    @client.on(events.NewMessage(pattern=r"\.listfiles"))
    async def list_files(event):
        if event.sender_id != OWNER_ID:
            return
        files = os.listdir(FILES_DIR)
        if not files:
            await event.reply("📂 **No files found in storage.**")
        else:
            file_list = "\n".join([f"- `{f}`" for f in files])
            await event.reply(f"📂 **Saved Files:**\n{file_list}")
        await asyncio.sleep(0.5)
        await event.delete()

    # ========== DELETE FILE ==========
    @client.on(events.NewMessage(pattern=r"\.delfile (.+)"))
    async def delete_file(event):
        if event.sender_id != OWNER_ID:
            return
        filename = event.pattern_match.group(1).strip()
        file_path = os.path.join(FILES_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            await event.reply(f"🗑 **Deleted file:** `{filename}`")
        else:
            await event.reply(f"❌ **File `{filename}` not found.**")
        await asyncio.sleep(0.5)
        await event.delete()

