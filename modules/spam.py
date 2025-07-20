import asyncio
from telethon import events
from config import OWNER_ID, MAX_SPAM_MESSAGES, SPAM_DELAY

active_spam = False  # Flag to control spam state

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
    # Start Spam
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.spam (\d+) (.+)"))
    @is_owner
    async def start_spam(event):
        global active_spam
        count = int(event.pattern_match.group(1))
        message = event.pattern_match.group(2)

        if count > MAX_SPAM_MESSAGES:
            return await event.edit(f"❌ Max spam limit is {MAX_SPAM_MESSAGES} messages.")

        active_spam = True
        await event.edit(f"⚠️ Starting spam with `{count}` messages... Use `.stopspam` to stop early.")

        try:
            for i in range(count):
                if not active_spam:
                    await client.send_message(event.chat_id, "🛑 Spam stopped.")
                    break
                await client.send_message(event.chat_id, message)
                await asyncio.sleep(SPAM_DELAY)
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Stop Spam
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.stopspam$"))
    @is_owner
    async def stop_spam(event):
        global active_spam
        if not active_spam:
            return await event.edit("❌ No active spam to stop.")
        active_spam = False
        await event.edit("🛑 **Spam has been stopped.**")

