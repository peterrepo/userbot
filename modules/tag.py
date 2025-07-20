from telethon import events
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

    @client.on(events.NewMessage(pattern=r"^\.tagall ?(.*)"))
    @is_owner
    async def tag_all(event):
        """Tags all members in a group."""
        custom_msg = event.pattern_match.group(1).strip()
        if not custom_msg:
            custom_msg = "👋 **Attention Everyone!**"

        await event.edit("📢 **Tagging all members...**")

        try:
            participants = []
            async for user in client.iter_participants(event.chat_id):
                if user.bot:
                    continue
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                participants.append(mention)

            chunk_size = 5  # Mention 5 users per message to avoid flood limits
            for i in range(0, len(participants), chunk_size):
                chunk = participants[i:i+chunk_size]
                text = f"{custom_msg}\n" + " ".join(chunk)
                await client.send_message(event.chat_id, text)
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
