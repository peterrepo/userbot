import os
import json
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from config import OWNER_ID

# ======================
# DATA FILE PATHS
# ======================
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GMUTE_FILE = os.path.join(DATA_DIR, "gmute_list.json")
GBAN_FILE = os.path.join(DATA_DIR, "gban_list.json")

os.makedirs(DATA_DIR, exist_ok=True)

# ======================
# JSON UTILITIES
# ======================
def load_list(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)
        return []
    with open(file_path, "r") as f:
        return json.load(f)

def save_list(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# ======================
# GMUTE FUNCTIONS
# ======================
def add_gmute(user_id):
    gmute_list = load_list(GMUTE_FILE)
    if user_id not in gmute_list:
        gmute_list.append(user_id)
        save_list(GMUTE_FILE, gmute_list)
        return True
    return False

def remove_gmute(user_id):
    gmute_list = load_list(GMUTE_FILE)
    if user_id in gmute_list:
        gmute_list.remove(user_id)
        save_list(GMUTE_FILE, gmute_list)
        return True
    return False

# ======================
# GBAN FUNCTIONS
# ======================
def add_gban(user_id):
    gban_list = load_list(GBAN_FILE)
    if user_id not in gban_list:
        gban_list.append(user_id)
        save_list(GBAN_FILE, gban_list)
        return True
    return False

def remove_gban(user_id):
    gban_list = load_list(GBAN_FILE)
    if user_id in gban_list:
        gban_list.remove(user_id)
        save_list(GBAN_FILE, gban_list)
        return True
    return False

# ======================
# HANDLERS
# ======================
def register(client):
    @client.on(events.NewMessage(pattern=r"^\.gmute$"))
    async def gmute_handler(event):
        if event.sender_id != OWNER_ID:
            return
        reply = await event.get_reply_message()
        if not reply:
            await event.edit("❌ Reply to a user to GMute.")
            return
        user = await reply.get_sender()
        if add_gmute(user.id):
            await event.edit(f"🔇 **Globally muted** [{user.first_name}](tg://user?id={user.id})")
        else:
            await event.edit(f"⚠️ User [{user.first_name}](tg://user?id={user.id}) is already GMute'd.")

    @client.on(events.NewMessage(pattern=r"^\.gunmute$"))
    async def gunmute_handler(event):
        if event.sender_id != OWNER_ID:
            return
        reply = await event.get_reply_message()
        if not reply:
            await event.edit("❌ Reply to a user to unmute.")
            return
        user = await reply.get_sender()
        if remove_gmute(user.id):
            await event.edit(f"🔊 **Unmuted** [{user.first_name}](tg://user?id={user.id})")
        else:
            await event.edit("⚠️ User is not in GMute list.")

    @client.on(events.NewMessage(pattern=r"^\.gban$"))
    async def gban_handler(event):
        if event.sender_id != OWNER_ID:
            return
        reply = await event.get_reply_message()
        if not reply:
            await event.edit("❌ Reply to a user to GBan.")
            return
        user = await reply.get_sender()
        if add_gban(user.id):
            await event.edit(f"🚫 **Globally banned** [{user.first_name}](tg://user?id={user.id})")
            # Block in PM
            try:
                await client(functions.contacts.BlockRequest(user.id))
            except Exception as e:
                print(f"[GBan Block Error] {e}")
        else:
            await event.edit(f"⚠️ User [{user.first_name}](tg://user?id={user.id}) is already GBan'd.")

    @client.on(events.NewMessage(pattern=r"^\.gunban$"))
    async def gunban_handler(event):
        if event.sender_id != OWNER_ID:
            return
        reply = await event.get_reply_message()
        if not reply:
            await event.edit("❌ Reply to a user to unban.")
            return
        user = await reply.get_sender()
        if remove_gban(user.id):
            await event.edit(f"✅ **Unbanned** [{user.first_name}](tg://user?id={user.id})")
            # Unblock in PM
            try:
                await client(functions.contacts.UnblockRequest(user.id))
            except Exception as e:
                print(f"[Gunban Unblock Error] {e}")
        else:
            await event.edit("⚠️ User is not in GBan list.")

    @client.on(events.NewMessage(pattern=r"^\.glist$"))
    async def glist_handler(event):
        if event.sender_id != OWNER_ID:
            return
        gmute_list = load_list(GMUTE_FILE)
        gban_list = load_list(GBAN_FILE)
        msg = "**🔗 Global Lists:**\n\n"
        msg += f"**GMute List:** {len(gmute_list)} users\n"
        msg += "\n".join([f"- `{uid}`" for uid in gmute_list]) or "No muted users."
        msg += f"\n\n**GBan List:** {len(gban_list)} users\n"
        msg += "\n".join([f"- `{uid}`" for uid in gban_list]) or "No banned users."
        await event.edit(msg)

    # ======================
    # AUTO DELETE GMUTE USERS
    # ======================
    @client.on(events.NewMessage(incoming=True))
    async def auto_delete_gmute(event):
        gmute_list = load_list(GMUTE_FILE)
        if event.sender_id in gmute_list:
            try:
                await event.delete()
            except Exception as e:
                print(f"[GMute Delete Error] {e}")

    # ======================
    # AUTO BAN GBAN USERS
    # ======================
    @client.on(events.NewMessage(incoming=True))
    async def auto_block_gban(event):
        gban_list = load_list(GBAN_FILE)
        if event.sender_id in gban_list:
            try:
                if event.is_private:
                    await client(functions.contacts.BlockRequest(event.sender_id))
                else:
                    # Ban user in groups where owner is admin
                    rights = ChatBannedRights(
                        until_date=None,
                        view_messages=True
                    )
                    await client(EditBannedRequest(event.chat_id, event.sender_id, rights))
            except Exception as e:
                print(f"[GBan Auto Ban Error] {e}")
