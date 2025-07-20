import asyncio
from telethon import events
from config import OWNER_ID

# Track active DM spam tasks
dmspam_tasks = {}

def register(client):
    @client.on(events.NewMessage(pattern=r"\.dmspam"))
    async def start_dmspam(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only command

        args = event.raw_text.split(" ", 3)
        if len(args) < 4:
            await event.reply("**Usage:** `.dmspam <user_id/username> <count> <message>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        user = args[1]
        try:
            count = int(args[2])
        except ValueError:
            await event.reply("⚠ **Count must be a number!**")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        message = args[3]
        await event.reply(f"🚀 **Starting DM spam to** `{user}` **for {count} messages.**")

        async def spam_user():
            for i in range(count):
                if event.sender_id in dmspam_tasks and dmspam_tasks[event.sender_id]["active"]:
                    try:
                        await client.send_message(user, message)
                        await asyncio.sleep(0.5)  # Delay between messages
                    except Exception as e:
                        await event.respond(f"❌ **Error:** {e}")
                        break
                else:
                    break
            await event.respond(f"✅ **DM spam completed for `{user}`.**")

        dmspam_tasks[event.sender_id] = {"active": True}
        asyncio.create_task(spam_user())
        await asyncio.sleep(0.5)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.stopdmspam"))
    async def stop_dmspam(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only command

        if event.sender_id in dmspam_tasks:
            dmspam_tasks[event.sender_id]["active"] = False
            await event.reply("🛑 **Stopped DM spam.**")
        else:
            await event.reply("⚠ **No active DM spam found.**")

        await asyncio.sleep(0.5)
        await event.delete()
