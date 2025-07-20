import json
import os
from telethon import events
from config import OWNER_ID

TAGALERT_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tagalert.json")

# Load or create tagalert data
def load_tagalert():
    if not os.path.exists(TAGALERT_FILE):
        return {"keywords": []}
    with open(TAGALERT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tagalert(data):
    with open(TAGALERT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

tagalert_data = load_tagalert()

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
    # Add Keyword
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.addalert (.+)"))
    @is_owner
    async def add_alert(event):
        keyword = event.pattern_match.group(1).strip().lower()
        if keyword in tagalert_data["keywords"]:
            return await event.edit(f"⚠️ `{keyword}` is already in alert list.")
        tagalert_data["keywords"].append(keyword)
        save_tagalert(tagalert_data)
        await event.edit(f"✅ Added alert for keyword: `{keyword}`")

    # -------------------
    # Remove Keyword
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.delalert (.+)"))
    @is_owner
    async def del_alert(event):
        keyword = event.pattern_match.group(1).strip().lower()
        if keyword not in tagalert_data["keywords"]:
            return await event.edit(f"❌ `{keyword}` not found in alert list.")
        tagalert_data["keywords"].remove(keyword)
        save_tagalert(tagalert_data)
        await event.edit(f"🗑 Removed alert for keyword: `{keyword}`")

    # -------------------
    # List Alerts
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.listalerts$"))
    @is_owner
    async def list_alerts(event):
        if not tagalert_data["keywords"]:
            return await event.edit("⚠️ No active tag alerts set.")
        alerts = "\n".join(f"• `{kw}`" for kw in tagalert_data["keywords"])
        await event.edit(f"**🔔 Current Tag Alerts:**\n{alerts}")

    # -------------------
    # Trigger Alert
    # -------------------
    @client.on(events.NewMessage())
    async def check_tag_alert(event):
        if event.sender_id == OWNER_ID:
            return  # Ignore self
        if not tagalert_data["keywords"]:
            return
        text = (event.raw_text or "").lower()
        for keyword in tagalert_data["keywords"]:
            if keyword in text:
                await client.send_message(
                    OWNER_ID,
                    f"**🔔 Tag Alert Triggered!**\n"
                    f"Keyword: `{keyword}`\n"
                    f"From: [{event.sender_id}](tg://user?id={event.sender_id})\n"
                    f"Chat: `{event.chat_id}`\n"
                    f"Message: {event.raw_text}"
                )
                break
