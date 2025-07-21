import asyncio
import time
import threading
from datetime import datetime
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import API_ID, API_HASH, SESSION_STRING, OWNER_ID

# ======================
# Start time for uptime
# ======================
START_TIME = time.time()

# ======================
# Import ALL modules
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
# Initialize Telethon client
# ======================
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ======================
# Dynamic Module Loader
# ======================
def register_modules():
    loaded_count = 0
    for module_name in ALL_MODULES:
        try:
            module = __import__(f"modules.{module_name}", fromlist=["register"])
            if hasattr(module, "register"):
                module.register(client)
            print(f"✅ Loaded: {module_name}")
            loaded_count += 1
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")
    return loaded_count

# ======================
# Owner-only Command Guard
# ======================
@client.on(events.NewMessage(pattern=r"^\.(\w+)"))
async def guard(event):
    if event.sender_id != OWNER_ID:
        return  # Silently ignore non-owner commands

# ======================
# .alive Command
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

# ======================
# Auto-Pinger (Keep Alive)
# ======================
async def auto_ping():
    while True:
        try:
            await client.send_message("me", f"🤖 Auto-ping at {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[Auto-Ping Error] {e}")
        await asyncio.sleep(300)  # 5 minutes

# ======================
# Flask Keepalive Server
# ======================
app = Flask(__name__)

@app.route('/')
def home():
    return "UserBot is running!"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# ======================
# Start Bot
# ======================
async def start_bot():
    print("🔄 Starting UserBot...")
    await client.start()
    print("🔐 Logged in successfully!")
    loaded = register_modules()
    print(f"📦 Loaded {loaded}/{len(ALL_MODULES)} modules.")
    asyncio.create_task(auto_ping())
    await client.run_until_disconnected()

if __name__ == "__main__":
    # Start Flask server in a separate thread
    threading.Thread(target=run_flask).start()

    try:
        client.loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
