import qrcode
import os
from PIL import Image
from pyzbar.pyzbar import decode
from telethon import events
from config import OWNER_ID

TEMP_QR = os.path.join(os.path.dirname(__file__), "..", "downloads", "qrcode.png")
os.makedirs(os.path.dirname(TEMP_QR), exist_ok=True)

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
    # Generate QR Code
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.qrcode (.+)"))
    @is_owner
    async def generate_qrcode(event):
        text = event.pattern_match.group(1)
        await event.edit("🔲 Generating QR code...")
        try:
            img = qrcode.make(text)
            img.save(TEMP_QR)
            await client.send_file(event.chat_id, TEMP_QR, caption=f"📤 QR Code for:\n`{text}`")
            os.remove(TEMP_QR)
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Decode QR Code
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.decodeqr$"))
    @is_owner
    async def decode_qrcode(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await event.edit("❌ Reply to a QR code image to decode it.")

        await event.edit("🔍 Decoding QR code...")
        try:
            file_path = await reply.download_media(file=TEMP_QR)
            img = Image.open(file_path)
            decoded = decode(img)

            if decoded:
                text = decoded[0].data.decode('utf-8')
                await event.edit(f"✅ Decoded QR Content:\n`{text}`")
            else:
                await event.edit("❌ No QR code detected in the image.")

            os.remove(file_path)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
