from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from config import OWNER_ID

def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.chatstats$"))
    @is_owner
    async def chat_stats(event):
        chat = await event.get_chat()
        await event.edit("📊 Fetching chat statistics...")

        try:
            if hasattr(chat, 'participants_count'):
                members_count = chat.participants_count
            else:
                members_count = len(await client.get_participants(event.chat_id))

            admins = []
            async for user in client.iter_participants(event.chat_id, filter=types.ChannelParticipantsAdmins):
                admins.append(user)

            msg = (
                f"**Chat Statistics:**\n"
                f"Title: {chat.title if hasattr(chat, 'title') else 'N/A'}\n"
                f"Type: {'Channel' if chat.broadcast else 'Group'}\n"
                f"Members: {members_count}\n"
                f"Admins: {len(admins)}\n"
            )
            await event.edit(msg)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.userstats(?: (.+))?"))
    @is_owner
    async def user_stats(event):
        input_arg = event.pattern_match.group(1)
        if input_arg:
            try:
                entity = await client.get_entity(input_arg)
            except Exception:
                return await event.edit("❌ Invalid user.")
        else:
            entity = await event.get_sender()

        await event.edit("📊 Fetching user statistics...")
        try:
            full = await client(GetFullUserRequest(entity.id))
            user = full.user
            profile = full.profile

            msg = (
                f"**User Statistics:**\n"
                f"Name: {user.first_name} {user.last_name or ''}\n"
                f"Username: @{user.username or 'N/A'}\n"
                f"User ID: {user.id}\n"
                f"Bio: {profile.about or 'N/A'}\n"
                f"Common Chats: {full.common_chats_count}\n"
                f"Is Bot: {'Yes' if user.bot else 'No'}\n"
            )
            await event.edit(msg)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
