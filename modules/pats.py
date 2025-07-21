# pats.py — Pat, Kiss, Hug, and "F" lines module (Owner only)
import random
from telethon import events
from config import OWNER_ID

# Define responses
PATS = [
    "🤗 gently pats you on the head.",
    "👐 gives you a big warm pat!",
    "😺 purrs and pats your face.",
]

KISSES = [
    "💋 plants a soft kiss on your cheek.",
    "😘 kisses you deeply.",
    "😽 smooches you affectionately.",
]

HUGS = [
    "🤗 gives you a tight warm hug.",
    "👐 wraps arms around you in a cuddle.",
    "🤝 offers a comforting embrace.",
]

FUCKS = [
    "🔞 grabs you and... you know the rest 😏",
    "💦 moans... damn.",
    "😈 gets freaky under the sheets.",
]


def register(client):
    @client.on(events.NewMessage(pattern=r"^\.pat$"))
    async def pat_handler(event):
        if event.sender_id != OWNER_ID:
            return
        await event.respond(random.choice(PATS))

    @client.on(events.NewMessage(pattern=r"^\.kiss$"))
    async def kiss_handler(event):
        if event.sender_id != OWNER_ID:
            return
        await event.respond(random.choice(KISSES))

    @client.on(events.NewMessage(pattern=r"^\.hug$"))
    async def hug_handler(event):
        if event.sender_id != OWNER_ID:
            return
        await event.respond(random.choice(HUGS))

    @client.on(events.NewMessage(pattern=r"^\.fuck$"))
    async def fuck_handler(event):
        if event.sender_id != OWNER_ID:
            return
        await event.respond(random.choice(FUCKS))
