import json
import os
from telethon import events
from config import OWNER_ID

USERDB_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "userdb.json")

# Load or initialize user database
def load_userdb():
    if not os.path.exists(USERDB_FILE):
        return {}
    with open(USERDB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def save_userdb(data):
    with open(USERDB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

userdb = load_userdb()

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    # -------------------
    # Track user info
    # -------------------
    @client.on(events.ChatAction())
    async def track_user_info(event):
        user = await event.get_user()
        if not user:
            return
        user_id = str(user.id)
        current_name = user.first_name or "Unknown"
        current_username = user.username or "None"

        if user_id not in userdb:
            userdb[user_id] = {
                "names": [current_name],
                "usernames": [current_username],
            }
        else:
            if current_name not in userdb[user_id]["names"]:
                userdb[user_id]["names"].append(current_name)
            if current_username not in userdb[user_id]["usernames"]:
                userdb[user_id]["usernames"].append(current_username)

        save_userdb(userdb)

    # -------------------
    # Show Name History
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.namehistory$"))
    @is_owner
    async def show_name_history(event):
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a user to see their name history.")
        user = await reply.get_sender()
        user_id = str(user.id)

        if user_id not in userdb:
            return await event.edit("❌ No history found for this user.")

        names = "\n".join(userdb[user_id]["names"])
        usernames = "\n".join(userdb[user_id]["usernames"])

        msg = f"**Name History for {user.first_name} (ID: {user.id}):**\n\n"
        msg += f"**Names:**\n{names}\n\n**Usernames:**\n{usernames}"
        await event.edit(msg)

    # -------------------
    # Clear User History
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.clearhistory$"))
    @is_owner
    async def clear_history(event):
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a user to clear their history.")
        user = await reply.get_sender()
        user_id = str(user.id)

        if user_id in userdb:
            del userdb[user_id]
            save_userdb(userdb)
            await event.edit(f"🧹 Cleared history for user `{user.id}`.")
        else:
            await event.edit("❌ No history found for this user.")
