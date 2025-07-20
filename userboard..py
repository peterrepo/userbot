import asyncio
import time
from datetime import datetime
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
from modules import (
    afk, animation, anime_cf, antipm, autopic, autoscroll, autosaver, basic,
    broadcast, carbon, clone, create, destruct, dictionary, dmspam, emoji,
    encryption, extrafun, files, ghost, gifs, git, globals, google, group,
    image, info, insta, invite, joinleave, locks, lyrics, memify, meme,
    mention, metrics, music, paste, pats, ping, profile, purge, qrcode,
    quotly, raid, reaction, replyraid, restart, sangmata, screenshot, spam,
    start, stats, sticker, stickers, tag, tagalert, tagall, text, tiny,
    translate, truthgame, update, upload, vctools, vulgar, weather, wiki,
    youtube
)

# ======================
# Initialize Telethon client
# ======================
if SESSION_STRING:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
else:
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ======================
# Register all modules dynamically
# ======================
def register_modules():
    modules = [
        afk, animation, anime_cf, antipm, autopic, autoscroll, autosaver, basic,
        broadcast, carbon, clone, create, destruct, dictionary, dmspam, emoji,
        encryption, extrafun, files, ghost, gifs, git, globals, google, group,
        image, info, insta, invite, joinleave, locks, lyrics, memify, meme,
        mention, metrics, music, paste, pats, ping, profile, purge, qrcode,
        quotly, raid, reaction, replyraid, restart, sangmata, screenshot, spam,
        start, stats, sticker, stickers, tag, tagalert, tagall, text, tiny,
        translate, truthgame, update, upload, vctools, vulgar, weather, wiki,
        youtube
    ]
    count = 0
    for module in modules:
        try:
            if hasattr(module, "register"):
                module.register(client)
            print(f"✅ Loaded: {module.__name__}")
            count += 1
        except Exception as e:
            print(f"❌ Failed to load {module.__name__}: {e}")
    return count

# ======================
# Owner-only command check
# ======================
@client.on(events.NewMessage(pattern=r"^\.(\w+)"))
async def owner_only(event):
    if event.sender_id != OWNER_ID:
        return  # Ignore commands from others
    await asyncio.sleep(0.5)
    await event.delete()

# ======================
# .alive Command
# ======================
@client.on(events.NewMessage(pattern=r"^\.alive$"))
async def alive_command(event):
    if event.sender_id != OWNER_ID:
        return
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - START_TIME))
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    module_count = len([m for m in [
        afk, animation, anime_cf, antipm, autopic, autoscroll, autosaver, basic,
        broadcast, carbon, clone, create, destruct, dictionary, dmspam, emoji,
        encryption, extrafun, files, ghost, gifs, git, globals, google, group,
        image, info, insta, invite, joinleave, locks, lyrics, memify, meme,
        mention, metrics, music, paste, pats, ping, profile, purge, qrcode,
        quotly, raid, reaction, replyraid, restart, sangmata, screenshot, spam,
        start, stats, sticker, stickers, tag, tagalert, tagall, text, tiny,
        translate, truthgame, update, upload, vctools, vulgar, weather, wiki,
        youtube
    ]])
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
# Start Bot
# ======================
async def start_bot():
    print("🔄 Starting UserBot...")
    await client.start()
    print("🔐 Logged in successfully!")
    module_count = register_modules()
    print(f"📦 Loaded {module_count} modules.")
    asyncio.create_task(auto_ping())
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        client.loop.run_until_complete(start_bot())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
