from telethon import events, types
from config import OWNER_ID

# ====== Owner check decorator ======
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

# Mapping lockable permissions to ChatBannedRights fields
LOCKABLE_RIGHTS = {
    "messages": "send_messages",
    "media": "send_media",
    "stickers": "send_stickers",
    "gifs": "send_gifs",
    "games": "send_games",
    "inline": "send_inline",
    "polls": "send_polls",
    "alerts": "send_polls",  # same as polls
    "all": "all",
}

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.lock (.+)"))
    @is_owner
    async def lock_permission(event):
        perm = event.pattern_match.group(1).lower()
        chat = await event.get_chat()
        rights = types.ChatBannedRights(
            until_date=None,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            send_polls=False,
            change_info=False,
            invite_users=False,
            pin_messages=False,
        )

        if perm == "all":
            # Ban all send permissions
            await event.client(EditBannedRequest(chat.id, event.sender_id, rights))
            await event.edit("🔒 Locked **all** permissions!")
            return

        if perm not in LOCKABLE_RIGHTS:
            await event.edit(f"❌ Unknown permission: {perm}")
            return

        # Create banned rights with only selected permission disabled
        kwargs = {LOCKABLE_RIGHTS[perm]: True}  # True disables permission in ChatBannedRights
        # Because ChatBannedRights disables if the field is True, invert logic
        banned_rights = types.ChatBannedRights(until_date=None, **kwargs)

        try:
            await event.client.edit_permissions(chat.id, "all", banned_rights)
            await event.edit(f"🔒 Locked **{perm}**!")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.unlock (.+)"))
    @is_owner
    async def unlock_permission(event):
        perm = event.pattern_match.group(1).lower()
        chat = await event.get_chat()

        if perm == "all":
            try:
                await event.client.edit_permissions(chat.id, "all", view_messages=True, send_messages=True)
                await event.edit("🔓 Unlocked **all** permissions!")
            except Exception as e:
                await event.edit(f"❌ Error: {e}")
            return

        if perm not in LOCKABLE_RIGHTS:
            await event.edit(f"❌ Unknown permission: {perm}")
            return

        # Allow that permission again
        try:
            await event.client.edit_permissions(chat.id, "all", **{LOCKABLE_RIGHTS[perm]: True})
            await event.edit(f"🔓 Unlocked **{perm}**!")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
