from telethon import events, functions, types
from config import OWNER_ID

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.mentionall$"))
    @is_owner
    async def mention_all(event):
        chat = await event.get_chat()
        if not (hasattr(chat, 'participants_count') or hasattr(chat, 'participants')):
            return await event.edit("❌ Can't fetch participants for this chat.")
        await event.edit("🔄 Mentioning all members, please wait...")

        try:
            members = await client.get_participants(event.chat_id)
            mentions = []
            for user in members:
                if user.bot:
                    continue
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                mentions.append(mention)
            # Telegram message limit ~4096 chars, send in chunks of 5 mentions each
            chunk_size = 5
            for i in range(0, len(mentions), chunk_size):
                chunk = mentions[i:i+chunk_size]
                await event.client.send_message(event.chat_id, " ".join(chunk))
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    @client.on(events.NewMessage(pattern=r"^\.mention (.+)"))
    @is_owner
    async def mention_users(event):
        args = event.pattern_match.group(1)
        user_ids = [int(u) for u in args.split() if u.isdigit()]
        if not user_ids:
            return await event.edit("❌ Provide user IDs separated by space.")

        mentions = []
        for uid in user_ids:
            try:
                user = await client.get_entity(uid)
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                mentions.append(mention)
            except:
                continue

        if mentions:
            await event.edit(" ".join(mentions))
        else:
            await event.edit("❌ No valid users found.")
