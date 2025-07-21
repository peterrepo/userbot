"""
UserBot - Complete Dynamic Userbot Loader
(C) 2025 Godhunter / Alpha UserBot Project
"""

import asyncio
import time
import importlib
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask
import threading

# ======================
# CONFIGURATION
# ======================
from config import API_ID, API_HASH, SESSION_STRING, OWNER_ID

# ======================
# BOT START TIME
# ======================
START_TIME = time.time()

# ======================
# MODULES LIST
# ======================
ALL_MODULES = [
    "afk", "animation", "anime_cf", "antipm", "autopic", "autoscroll",
    "autosaver", "basic", "broadcast", "carbon", "clone", "create",
    "destruct", "dictionary", "dmspam", "emoji", "encryption", "extrafun",
    "files", "ghost", "gifs", "git", "globals", "google", "group",
    "image", "info", "insta", "invite", "joinleave", "locks",
    "lyrics", "memify", "meme", "mention", "metrics", "music",
    "paste", "pats", "ping", "profile", "purge", "qrcode",
    "quotly", "raid", "reaction", "replyraid", "restart", "sangmata",
    "screenshot", "spam", "start", "stats", "sticker", "stickers",
    "tag", "tagalert", "tagall", "text", "tiny", "translate",
    "truthgame", "update", "upload", "vctools", "vulgar", "weather",
    "wiki", "youtube"
]

# ======================
# TELETHON CLIENT
# ======================
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ======================
# DYNAMIC MODULE LOADER
# ======================
def register_modules():
    loaded_count = 0
    for module_name in ALL_MODULES:
        try:
            module = importlib.import_module(f"modules.{module_name}")
            if hasattr(module, "register"):
                module.register(client)
            print(f"✅ Loaded: {module_name}")
            loaded_count += 1
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")
    return loaded_count

# ======================
# OWNER-ONLY COMMAND GUARD
# ======================
@client.on(events.NewMessage(pattern=r"^\.(\w+)"))
async def guard(event):
    if event.sender_id != OWNER_ID:
        return  # Ignore messages from non-owner
    await asyncio.sleep(2)
    try:
        await event.delete()  # Auto-delete after 2 seconds
    except:
        pass

# ======================
# .ALIVE COMMAND
# ======================
@client.on(events.NewMessage(pattern=r"^\.alive$"))
async def alive_command(event):
    if event.sender_id != OWNER_ID:
        return
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - START_TIME))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module_count = len([m for m in ALL_MODULES])
    await event.respond(
        f"**🤖 UserBot is Alive!**\n\n"
        f"**Uptime:** `{uptime}`\n"
        f"**Modules Loaded:** `{module_count}`\n"
        f"**Current Time:** `{now}`"
    )
    await asyncio.sleep(2)
    try:
        await event.delete()
    except:
        pass

# ======================
# KEEP-ALIVE SERVER
# ======================
app = Flask('')

@app.route('/')
def home():
    return "🤖 UserBot KeepAlive Server Running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

# ======================
# START BOT
# ======================
async def start_bot():
    print("🔄 Starting UserBot...")
    await client.start()
    print("🔐 Logged in successfully!")
    loaded = register_modules()
    print(f"📦 Loaded {loaded}/{len(ALL_MODULES)} modules.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    keep_alive()  # Start KeepAlive for UptimeRobot
    try:
        client.loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
