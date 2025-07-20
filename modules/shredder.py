import os
from telethon import events
from userbot import bot

SHREDDER_FILE = "data/shredder_patterns.txt"

# Ensure the file exists
os.makedirs("data", exist_ok=True)
if not os.path.exists(SHREDDER_FILE):
    with open(SHREDDER_FILE, "w") as f:
        f.write("password\nsecret\napi_key\n")  # Default patterns

# Global variable to track shredding status
SHRED_ACTIVE = False

def load_patterns():
    with open(SHREDDER_FILE, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def shred_text(text):
    patterns = load_patterns()
    for pattern in patterns:
        text = text.replace(pattern, "****")
    return text

@bot.on(events.NewMessage(pattern=r"\.shred (on|off)$"))
async def toggle_shred(event):
    global SHRED_ACTIVE
    state = event.pattern_match.group(1)
    if state == "on":
        SHRED_ACTIVE = True
        await event.reply("🛡 **Shredder Enabled!** Sensitive text will be censored.")
    else:
        SHRED_ACTIVE = False
        await event.reply("🛑 **Shredder Disabled!** Messages will not be censored.")

@bot.on(events.NewMessage(outgoing=True))
async def shred_outgoing(event):
    if SHRED_ACTIVE and event.raw_text:
        new_text = shred_text(event.raw_text.lower())
        if new_text != event.raw_text.lower():
            await event.edit(new_text)
