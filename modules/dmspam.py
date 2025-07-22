import asyncio
from telethon import events
from config import OWNER_ID

# Global flag to control spam cancellation
STOP_DM_SPAM = False

def register(client):
    global STOP_DM_SPAM

    @client.on(events.NewMessage(pattern=r"^\.dmspam (\d+) (.+)"))
    async def dm_spam_handler(event):
        global STOP_DM_SPAM

        if event.sender_id != OWNER_ID:
            return

        if not event.is_reply:
            await event.edit("❌ **Reply to a user’s message to spam their DM.**")
            return

        try:
            reply_msg = await event.get_reply_message()
            user = await client.get_entity(reply_msg.sender_id)

            count = int(event.pattern_match.group(1))
            message = event.pattern_match.group(2)

            STOP_DM_SPAM = False
            await event.edit(f"🚀 **Spamming {user.first_name}'s DM {count} times...**")

            for i in range(count):
                if STOP_DM_SPAM:
                    await event.respond("🛑 **DM spam stopped by owner.**")
                    break

                try:
                    await client.send_message(user.id, message)
                    await asyncio.sleep(0.5)
                except Exception as e:
                    await event.respond(f"⚠️ Error at message {i+1}: {e}")
                    break

            else:
                await event.respond(f"✅ **Finished spamming {user.first_name}.**")

        except Exception as e:
            await event.edit(f"⚠️ **Error:** {e}")

    @client.on(events.NewMessage(pattern=r"^\.stopdmspam$"))
    async def stop_dm_spam(event):
        global STOP_DM_SPAM
        if event.sender_id != OWNER_ID:
            return
        STOP_DM_SPAM = True
        await event.respond("🛑 **DM Spam has been stopped.**")

