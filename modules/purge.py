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

    # -------------------
    # Purge Messages
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.purge$"))
    @is_owner
    async def purge_messages(event):
        """Deletes all messages starting from a replied message."""
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a message to start purging from.")

        await event.edit("🗑 Purging messages...")
        try:
            count = 0
            async for msg in client.iter_messages(event.chat_id, min_id=reply.id):
                await msg.delete()
                count += 1
            await event.delete()
            confirmation = await client.send_message(event.chat_id, f"✅ Purged {count} messages.")
            await confirmation.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Del (delete reply)
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.del$"))
    @is_owner
    async def delete_message(event):
        """Deletes the replied message."""
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a message to delete it.")
        try:
            await reply.delete()
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

