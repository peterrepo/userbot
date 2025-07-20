import asyncio
import base64
from telethon import events
from cryptography.fernet import Fernet
from config import OWNER_ID, ENCRYPTION_KEY

# Generate a default key if not provided
if not ENCRYPTION_KEY:
    key = Fernet.generate_key()
else:
    key = ENCRYPTION_KEY.encode()

fernet = Fernet(key)

def register(client):
    @client.on(events.NewMessage(pattern=r"\.encrypt"))
    async def encrypt_message(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.raw_text.split(" ", 1)
        if len(args) < 2:
            await event.reply("**Usage:** `.encrypt <message>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        message = args[1].encode()
        encrypted_text = fernet.encrypt(message).decode()
        await event.reply(f"🔐 **Encrypted:**\n`{encrypted_text}`")
        await asyncio.sleep(0.5)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.decrypt"))
    async def decrypt_message(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.raw_text.split(" ", 1)
        if len(args) < 2:
            await event.reply("**Usage:** `.decrypt <encrypted_text>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        encrypted_text = args[1].encode()
        try:
            decrypted_text = fernet.decrypt(encrypted_text).decode()
        except Exception:
            await event.reply("⚠ **Invalid or corrupted encrypted text!**")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        await event.reply(f"🔓 **Decrypted:**\n`{decrypted_text}`")
        await asyncio.sleep(0.5)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.b64encode"))
    async def base64_encode(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.raw_text.split(" ", 1)
        if len(args) < 2:
            await event.reply("**Usage:** `.b64encode <text>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        encoded = base64.b64encode(args[1].encode()).decode()
        await event.reply(f"🔐 **Base64 Encoded:**\n`{encoded}`")
        await asyncio.sleep(0.5)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.b64decode"))
    async def base64_decode(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.raw_text.split(" ", 1)
        if len(args) < 2:
            await event.reply("**Usage:** `.b64decode <encoded_text>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        try:
            decoded = base64.b64decode(args[1].encode()).decode()
        except Exception:
            await event.reply("⚠ **Invalid Base64 string!**")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        await event.reply(f"🔓 **Base64 Decoded:**\n`{decoded}`")
        await asyncio.sleep(0.5)
        await event.delete()

