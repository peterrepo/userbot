import requests
from telethon import events
from config import OWNER_ID

QUOTLY_API = "https://bot.lyo.su/quote/generate"  # Free Quotly API endpoint

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.q$"))
    @is_owner
    async def quote_message(event):
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a message to quote it.")

        await event.edit("📝 Generating quote sticker...")
        try:
            # Prepare data for API
            payload = {
                "messages": [
                    {
                        "text": reply.message,
                        "replyMessage": None,
                        "from": {
                            "id": reply.sender_id,
                            "name": reply.sender.first_name if reply.sender else "Unknown",
                            "photo": True
                        }
                    }
                ]
            }

            res = requests.post(QUOTLY_API, json=payload)
            if res.status_code != 200:
                return await event.edit("❌ Failed to create quote.")

            file_url = res.json()["result"]["image"]
            await client.send_file(event.chat_id, file_url)
            await event.delete()

        except Exception as e:
            await event.edit(f"❌ Error: {e}")
