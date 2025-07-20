import json
from telethon import events
from config import OWNER_ID
from telethon.tl.types import ChatAdminRights

def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.promote$"))
    @is_owner
    async def promote_user(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to a user to promote.")
        reply = await event.get_reply_message()
        try:
            rights = ChatAdminRights(
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                invite_users=True
            )
            await event.client.edit_admin(event.chat_id, reply.sender_id, rights)
            await event.reply(f"✅ Promoted {reply.sender.first_name}!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.demote$"))
    @is_owner
    async def demote_user(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to a user to demote.")
        reply = await event.get_reply_message()
        try:
            rights = ChatAdminRights()
            await event.client.edit_admin(event.chat_id, reply.sender_id, rights)
            await event.reply(f"✅ Demoted {reply.sender.first_name}!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.ban$"))
    @is_owner
    async def ban_user(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to a user to ban.")
        reply = await event.get_reply_message()
        try:
            await event.client.edit_permissions(event.chat_id, reply.sender_id, view_messages=False)
            await event.reply(f"🚫 Banned {reply.sender.first_name}!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.unban$"))
    @is_owner
    async def unban_user(event):
        if len(event.message.text.split()) < 2 and not event.reply_to_msg_id:
            return await event.reply("Usage: `.unban <user_id>` or reply to a banned user.")
        try:
            user_id = None
            if event.reply_to_msg_id:
                reply = await event.get_reply_message()
                user_id = reply.sender_id
            else:
                user_id = int(event.message.text.split()[1])
            await event.client.edit_permissions(event.chat_id, user_id, view_messages=True)
            await event.reply(f"✅ Unbanned `{user_id}`!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.kick$"))
    @is_owner
    async def kick_user(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to a user to kick.")
        reply = await event.get_reply_message()
        try:
            await event.client.kick_participant(event.chat_id, reply.sender_id)
            await event.reply(f"👢 Kicked {reply.sender.first_name}!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.pin$"))
    @is_owner
    async def pin_message(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to a message to pin.")
        try:
            reply = await event.get_reply_message()
            await reply.pin()
            await event.reply("📌 Message pinned!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.unpin$"))
    @is_owner
    async def unpin_message(event):
        try:
            await event.client.unpin_message(event.chat_id)
            await event.reply("📌 Message unpinned!")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")
