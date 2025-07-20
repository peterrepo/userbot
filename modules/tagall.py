from telethon import events
from config import OWNER_ID
import asyncio

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.tagall2 ?(.*)"))
    @is_owner
    async def tag_all(event):
        """
        Tags all members in a group in batches of 10 users per message.
        """
        custom_msg = event.pattern_match.group(1).strip()
        if not custom_msg:
            custom_msg = "👋 **Hello Everyone!**"

        await event.edit("📢 **Starting advanced tag...**")

        try:
            participants = []
            async for user in client.iter_participants(event.chat_id):
                if user.bot:
                    continue
                mention = f"[{user.first_name}](tg://user?id={user.id})"
                participants.append(mention)

            # Send in batches of 10
            batch_size = 10
            for i in range(0, len(participants), batch_size):
                chunk = participants[i:i + batch_size]
                text = f"{custom_msg}\n" + " ".join(chunk)
                await client.send_message(event.chat_id, text)
                await asyncio.sleep(1)  # Avoid flood wait
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
