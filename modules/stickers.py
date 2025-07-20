import os
from telethon import events
from PIL import Image
from userbot import bot

TEMP_WEBP = "temp_sticker.webp"
TEMP_PNG = "temp_sticker.png"


@bot.on(events.NewMessage(pattern=r"\.to_sticker$"))
async def to_sticker(event):
    """Convert image/video/gif to a sticker"""
    reply = await event.get_reply_message()

    if not reply or not (reply.photo or reply.video or reply.gif):
        await event.reply("⚠ **Reply to an image/video/gif to convert it into a sticker.**")
        return

    temp_file = await bot.download_media(reply.media)
    try:
        img = Image.open(temp_file).convert("RGBA")
        img.save(TEMP_WEBP, "WEBP")
        await bot.send_file(event.chat_id, TEMP_WEBP)
        os.remove(TEMP_WEBP)
    except Exception as e:
        await event.reply(f"⚠ **Error converting to sticker:** {str(e)}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@bot.on(events.NewMessage(pattern=r"\.to_png$"))
async def to_png(event):
    """Extract a sticker as PNG"""
    reply = await event.get_reply_message()

    if not reply or not reply.sticker:
        await event.reply("⚠ **Reply to a sticker to extract it as PNG.**")
        return

    temp_file = await bot.download_media(reply.media)
    try:
        img = Image.open(temp_file).convert("RGBA")
        img.save(TEMP_PNG, "PNG")
        await bot.send_file(event.chat_id, TEMP_PNG)
        os.remove(TEMP_PNG)
    except Exception as e:
        await event.reply(f"⚠ **Error converting to PNG:** {str(e)}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


@bot.on(events.NewMessage(pattern=r"\.get_sticker_pack$"))
async def get_sticker_pack(event):
    """Fetch all stickers from a sticker pack"""
    reply = await event.get_reply_message()

    if not reply or not reply.sticker:
        await event.reply("⚠ **Reply to a sticker to fetch its pack.**")
        return

    try:
        stickerset = await bot(GetStickerSetRequest(reply.document.attributes[1].stickerset))
        await event.reply(f"**Sticker Pack:** {stickerset.set.title}\n**Short Name:** {stickerset.set.short_name}")
        await bot.send_file(event.chat_id, [s.document for s in stickerset.packs])
    except Exception as e:
        await event.reply(f"⚠ **Error fetching sticker pack:** {str(e)}")
