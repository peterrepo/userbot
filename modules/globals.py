import json
import os
from telethon import events
from config import OWNER_ID, DATA_DIR

GBAN_FILE = os.path.join(DATA_DIR, "gban_list.json")
GMUTE_FILE = os.path.join(DATA_DIR, "gmute_list.json")

# Ensure files exist
for file in [GBAN_FILE, GMUTE_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

def load_list(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_list(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def register(client):
    @client.on(events.NewMessage(pattern=r"\.gban(?: |$)(.*)"))
    async def global_ban(event):
        if event.sender_id != OWNER_ID:
            return

        reply = await event.get_reply_message()
        user = None
        reason = event.pattern_match.group(1) or "No reason provided"

        if reply:
            user = reply.sender_id
        elif event.is_private:
            user = event.chat_id

        if not user:
            await event.respond("❌ **Reply to a user or specify a user ID to gban.**")
            return

        gban_list = load_list(GBAN_FILE)
        if user in gban_list:
            await event.respond(f"⚠ **User {user} is already globally banned.**")
        else:
            gban_list.append(user)
            save_list(GBAN_FILE, gban_list)
            await event.respond(f"🚫 **User {user} has been globally banned.**\nReason: `{reason}`")

    @client.on(events.NewMessage(pattern=r"\.ungban(?: |$)(.*)"))
    async def global_unban(event):
        if event.sender_id != OWNER_ID:
            return

        reply = await event.get_reply_message()
        user = None
        if reply:
            user = reply.sender_id
        elif event.is_private:
            user = event.chat_id

        if not user:
            await event.respond("❌ **Reply to a user or specify a user ID to ungban.**")
            return

        gban_list = load_list(GBAN_FILE)
        if user not in gban_list:
            await event.respond(f"⚠ **User {user} is not in the global ban list.**")
        else:
            gban_list.remove(user)
            save_list(GBAN_FILE, gban_list)
            await event.respond(f"✅ **User {user} has been unbanned globally.**")

    @client.on(events.NewMessage(pattern=r"\.gmute(?: |$)(.*)"))
    async def global_mute(event):
        if event.sender_id != OWNER_ID:
            return

        reply = await event.get_reply_message()
        user = None
        if reply:
            user = reply.sender_id
        elif event.is_private:
            user = event.chat_id

        if not user:
            await event.respond("❌ **Reply to a user or specify a user ID to gmute.**")
            return

        gmute_list = load_list(GMUTE_FILE)
        if user in gmute_list:
            await event.respond(f"⚠ **User {user} is already globally muted.**")
        else:
            gmute_list.append(user)
            save_list(GMUTE_FILE, gmute_list)
            await event.respond(f"🔇 **User {user} has been globally muted.**")

    @client.on(events.NewMessage(pattern=r"\.ungmute(?: |$)(.*)"))
    async def global_unmute(event):
        if event.sender_id != OWNER_ID:
            return

        reply = await event.get_reply_message()
        user = None
        if reply:
            user = reply.sender_id
        elif event.is_private:
            user = event.chat_id

        if not user:
            await event.respond("❌ **Reply to a user or specify a user ID to ungmute.**")
            return

        gmute_list = load_list(GMUTE_FILE)
        if user not in gmute_list:
            await event.respond(f"⚠ **User {user} is not in the global mute list.**")
        else:
            gmute_list.remove(user)
            save_list(GMUTE_FILE, gmute_list)
            await event.respond(f"✅ **User {user} has been unmuted globally.**")

    @client.on(events.NewMessage())
    async def auto_delete_muted(event):
        if event.is_private:
            return
        gmute_list = load_list(GMUTE_FILE)
        if event.sender_id in gmute_list:
            await event.delete()
