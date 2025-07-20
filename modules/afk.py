import json
import os
from telethon import events
from config import OWNER_ID

AFK_FILE = "data/afk.json"

# Load or create AFK data
if not os.path.exists(AFK_FILE):
    with open(AFK_FILE, "w") as f:
        json.dump({"is_afk": False, "reason": ""}, f)


def load_afk():
    with open(AFK_FILE, "r") as f:
        return json.load(f)


def save_afk(data):
    with open(AFK_FILE, "w") as f:
        json.dump(data, f)


def register(client):
    # ======================
    # .afk command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.afk ?(.*)"))
    async def set_afk(event):
        if event.sender_id != OWNER_ID:
            return
        reason = event.pattern_match.group(1) or "AFK"
        afk_data = {"is_afk": True, "reason": reason}
        save_afk(afk_data)
        await event.respond(f"**AFK mode ON. Reason:** {reason}")
        await event.delete()

    # ======================
    # .back command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.back"))
    async def remove_afk(event):
        if event.sender_id != OWNER_ID:
            return
        save_afk({"is_afk": False, "reason": ""})
        await event.respond("**AFK mode OFF.**")
        await event.delete()

    # ======================
    # Auto-reply when AFK
    # ======================
    @client.on(events.NewMessage(incoming=True))
    async def afk_auto_reply(event):
        if event.sender_id == OWNER_ID:
            return
        afk_data = load_afk()
        if afk_data.get("is_afk", False):
            if event.is_private or (await event.get_sender()).id != OWNER_ID:
                await event.reply(f"**I am currently AFK. Reason:** {afk_data['reason']}")
