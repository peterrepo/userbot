import os
import requests
from telethon import events
from config import OWNER_ID, GDRIVE_API_KEY, GDRIVE_FOLDER_ID

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
    # Telegraph Upload
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.tgupload$"))
    @is_owner
    async def upload_to_telegraph(event):
        reply = await event.get_reply_message()
        if not reply or not (reply.photo or reply.document):
            return await event.edit("❌ Reply to an image or document to upload to Telegraph.")

        await event.edit("📤 **Uploading to Telegraph...**")
        try:
            file_path = await client.download_media(reply, "temp_upload")

            with open(file_path, "rb") as f:
                response = requests.post(
                    "https://telegra.ph/upload",
                    files={"file": ("file", f, "application/octet-stream")},
                )

            if response.status_code == 200:
                telegraph_url = "https://telegra.ph" + response.json()[0]["src"]
                await event.edit(f"✅ **Uploaded to Telegraph:**\n{telegraph_url}")
            else:
                await event.edit(f"❌ Telegraph upload failed: {response.text}")

            os.remove(file_path)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Google Drive Upload (basic)
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.gdrive$"))
    @is_owner
    async def upload_to_gdrive(event):
        reply = await event.get_reply_message()
        if not reply or not (reply.document or reply.video or reply.audio):
            return await event.edit("❌ Reply to a file to upload to Google Drive.")

        if not GDRIVE_API_KEY:
            return await event.edit("❌ Google Drive API Key not configured.")

        await event.edit("📤 **Uploading to Google Drive...**")
        try:
            file_path = await client.download_media(reply, "temp_upload")
            filename = os.path.basename(file_path)

            # This is a placeholder — real Google Drive upload requires OAuth flow.
            # For now, simulate an upload.
            await event.edit(f"✅ **Uploaded (Simulated):** `{filename}`")

            os.remove(file_path)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
