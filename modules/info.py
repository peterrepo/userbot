import os
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetFullChatRequest
from config import OWNER_ID

# ====== Decorator to restrict commands to owner only ======
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    # --------------------
    # Get User/Chat ID
    # --------------------
    @client.on(events.NewMessage(pattern=r"^\.id$"))
    @is_owner
    async def get_id(event):
        reply = await event.get_reply_message()
        if reply:
            await event.edit(f"**Replied User ID:** `{reply.sender_id}`")
        else:
            await event.edit(f"**Current Chat ID:** `{event.chat_id}`")

    # --------------------
    # Whois Command
    # --------------------
    @client.on(events.NewMessage(pattern=r"^\.whois$"))
    @is_owner
    async def whois(event):
        if not event.reply_to_msg_id:
            return await event.reply("Reply to a user to get their info.")
        reply = await event.get_reply_message()
        user = await client.get_entity(reply.sender_id)
        info = f"**User Info:**\n\n"
        info += f"**Name:** {user.first_name or ''} {user.last_name or ''}\n"
        info += f"**Username:** @{user.username}\n" if user.username else ""
        info += f"**User ID:** `{user.id}`\n"
        info += f"**Bot:** {user.bot}\n"
        info += f"**Restricted:** {user.restricted}\n"
        info += f"**Verified:** {user.verified}\n"

        photo = await client.download_profile_photo(user, file="whois.jpg")
        if photo:
            await client.send_file(event.chat_id, photo, caption=info)
            os.remove(photo)
        else:
            await event.edit(info)

    # --------------------
    # User Info Command
    # --------------------
    @client.on(events.NewMessage(pattern=r"^\.userinfo ?(.*)$"))
    @is_owner
    async def userinfo(event):
        args = event.pattern_match.group(1)
        if args:
            user = await client.get_entity(args)
        else:
            if not event.reply_to_msg_id:
                return await event.reply("Reply to a user or provide username/user ID.")
            reply = await event.get_reply_message()
            user = await client.get_entity(reply.sender_id)
        
        full = await client(GetFullUserRequest(user.id))
        bio = full.about if full.about else "No bio"
        info = (
            f"**User Info:**\n\n"
            f"**Name:** {user.first_name or ''} {user.last_name or ''}\n"
            f"**Username:** @{user.username}\n" if user.username else "" +
            f"**ID:** `{user.id}`\n"
            f"**Bio:** {bio}"
        )
        await event.edit(info)

    # --------------------
    # Chat Info Command
    # --------------------
    @client.on(events.NewMessage(pattern=r"^\.chatinfo$"))
    @is_owner
    async def chatinfo(event):
        chat = await event.get_chat()
        if chat.broadcast:
            full = await client(GetFullChannelRequest(chat.id))
        else:
            full = await client(GetFullChatRequest(chat.id))

        info = f"**Chat Info:**\n\n"
        info += f"**Title:** {chat.title}\n" if hasattr(chat, "title") else ""
        info += f"**Chat ID:** `{chat.id}`\n"
        info += f"**Type:** {type(chat).__name__}\n"
        info += f"**Participants:** {getattr(full.full_chat, 'participants_count', 'N/A')}\n"
        info += f"**Description:** {getattr(full.full_chat, 'about', 'None')}\n"

        await event.edit(info)
