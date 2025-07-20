from telethon import events
from config import OWNER_ID

# ====== Decorator for owner-only commands ======
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    # ----------------------
    # Join a Group/Channel
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.join (.+)"))
    @is_owner
    async def join_chat(event):
        invite_link = event.pattern_match.group(1)
        await event.edit(f"🔗 **Joining chat:** `{invite_link}`")
        try:
            await client.join_chat(invite_link)
            await event.edit(f"✅ **Successfully joined:** `{invite_link}`")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # ----------------------
    # Leave Current Chat
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.leave$"))
    @is_owner
    async def leave_current_chat(event):
        chat_id = event.chat_id
        await event.edit("👋 **Leaving this chat...**")
        try:
            await client.delete_dialog(chat_id)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # ----------------------
    # Leave Specific Chat by ID
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.leave (-?\d+)$"))
    @is_owner
    async def leave_specific_chat(event):
        chat_id = int(event.pattern_match.group(1))
        await event.edit(f"👋 **Leaving chat ID:** `{chat_id}`")
        try:
            await client.delete_dialog(chat_id)
            await event.edit(f"✅ **Left chat:** `{chat_id}`")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
