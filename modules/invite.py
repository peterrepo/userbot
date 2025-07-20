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
    # Invite Single User
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.invite (.+)"))
    @is_owner
    async def invite_user(event):
        username = event.pattern_match.group(1)
        await event.edit(f"➕ **Inviting:** `{username}` ...")
        try:
            await client(  # Telethon method
                client.invite_to_channel(event.chat_id, [username])
            )
            await event.edit(f"✅ Successfully invited `{username}`.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # ----------------------
    # Bulk Add Users
    # ----------------------
    @client.on(events.NewMessage(pattern=r"^\.addusers (.+)"))
    @is_owner
    async def add_users(event):
        users = event.pattern_match.group(1).split()
        if not users:
            return await event.edit("❌ Provide at least one username to add.")

        added = []
        failed = []
        await event.edit(f"➕ **Adding {len(users)} users...**")
        for user in users:
            try:
                await client(
                    client.invite_to_channel(event.chat_id, [user])
                )
                added.append(user)
            except Exception:
                failed.append(user)

        result_msg = "**Bulk Add Result:**\n\n"
        if added:
            result_msg += f"✅ **Added:** `{', '.join(added)}`\n"
        if failed:
            result_msg += f"❌ **Failed:** `{', '.join(failed)}`"
        await event.edit(result_msg)
