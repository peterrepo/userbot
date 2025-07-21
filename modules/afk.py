import os
import json
from datetime import datetime
from telethon import events

# ======================
# AFK FILE PATH
# ======================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # userbot/
DATA_DIR = os.path.join(BASE_DIR, "data")
AFK_FILE = os.path.join(DATA_DIR, "afk.json")

# ======================
# AFK STATE
# ======================
AFK_STATE = {
    "is_afk": False,
    "reason": "",
    "since": ""
}

# ======================
# Helper Functions
# ======================
def ensure_afk_file():
    if not os.path.exists(AFK_FILE):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(AFK_FILE, "w") as f:
            json.dump(AFK_STATE, f, indent=4)

def save_afk_state():
    ensure_afk_file()
    with open(AFK_FILE, "w") as f:
        json.dump(AFK_STATE, f, indent=4)

def load_afk_state():
    ensure_afk_file()
    with open(AFK_FILE, "r") as f:
        return json.load(f)

# ======================
# Register AFK Module
# ======================
def register(client):
    ensure_afk_file()

    @client.on(events.NewMessage(pattern=r"^\.afk(?: (.*))?$"))
    async def set_afk(event):
        reason = event.pattern_match.group(1) or "No reason provided."
        AFK_STATE.update({
            "is_afk": True,
            "reason": reason,
            "since": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_afk_state()
        await event.respond(f"**AFK activated.**\nReason: `{reason}`")

    @client.on(events.NewMessage(pattern=r"^\.back$"))
    async def remove_afk(event):
        AFK_STATE.update({"is_afk": False, "reason": "", "since": ""})
        save_afk_state()
        await event.respond("**Welcome back!** AFK mode is now off.")

    @client.on(events.NewMessage())
    async def afk_responder(event):
        state = load_afk_state()
        if not state.get("is_afk"):
            return

        # Check if the message should trigger AFK
        should_reply = False

        # Private message (DM)
        if event.is_private:
            should_reply = True

        # Mentioned in group chat
        elif event.message.mentioned:
            should_reply = True

        # Someone replied to your message
        elif event.is_reply:
            reply_msg = await event.get_reply_message()
            if reply_msg and reply_msg.sender_id == (await client.get_me()).id:
                should_reply = True

        if should_reply:
            reason = state.get("reason", "No reason.")
            since = state.get("since", "Unknown time.")
            await event.reply(f"**I am AFK.**\nReason: `{reason}`\nSince: `{since}`")
