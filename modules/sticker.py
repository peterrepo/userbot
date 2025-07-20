import os
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

    @client.on(events.NewMessage(pattern=r"^\.tosticker$"))
    @is_owner
    async def image_to_sticker(event):
        reply = await event.get_reply_message()
        if not reply or not (reply.photo or reply.sticker or reply.video):
            return await event.edit("❌ Reply to an image/video to convert it to a sticker.")

        await event.edit("🎨 **Converting to sticker...**")
        try:
            file_path = await client.download_media(reply, "temp_media")
            await client.send_file(
                event.chat_id,
                file_path,
                force_document=False,
                allow_cache=False,
                reply_to=reply.id,
                attributes=None
            )
            await event.delete()
            os.remove(file_path)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
