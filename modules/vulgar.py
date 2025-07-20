import random
from telethon import events
from config import OWNER_ID

# A list of random roast/insult lines
VULGAR_LINES = [
    "You're proof that even evolution takes breaks.",
    "I’d agree with you, but then we’d both be wrong.",
    "You have something on your chin... no, the third one down.",
    "Your secrets are safe with me. I never even listen when you tell me them.",
    "You bring everyone so much joy... when you leave the room.",
    "You're like a cloud. When you disappear, it's a beautiful day.",
    "Your brain is like a browser with 100 tabs open, all frozen.",
    "You're as useless as the 'ueue' in 'queue'.",
    "You have something that everyone needs — a mute button.",
    "You're like a clouded Wi-Fi connection: slow and frustrating."
]

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.vulgar$"))
    @is_owner
    async def send_vulgar(event):
        """Sends a random roast/insult."""
        line = random.choice(VULGAR_LINES)
        await event.edit(f"💢 **{line}**")

    @client.on(events.NewMessage(pattern=r"^\.vulgaradd (.+)"))
    @is_owner
    async def add_vulgar_line(event):
        """Adds a new roast/insult to the list."""
        new_line = event.pattern_match.group(1).strip()
        if new_line:
            VULGAR_LINES.append(new_line)
            await event.edit(f"✅ Added new vulgar line:\n`{new_line}`")
        else:
            await event.edit("❌ Please provide a valid insult/roast text.")
