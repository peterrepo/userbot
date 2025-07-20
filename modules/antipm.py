import asyncio
from telethon import events
from config import OWNER_ID

# State storage
ANTI_PM_ACTIVE = False
USER_WARNINGS = {}  # {user_id: warning_count}
MAX_WARNINGS = 3


def register(client):
    # ======================
    # Toggle Anti-PM
    # ======================
    @client.on(events.NewMessage(pattern=r"\.antipm (on|off)$"))
    async def toggle_antipm(event):
        global ANTI_PM_ACTIVE
        if event.sender_id != OWNER_ID:
            return
        state = event.pattern_match.group(1).lower()
        ANTI_PM_ACTIVE = state == "on"
        await event.edit(f"**Anti-PM is now {'ON' if ANTI_PM_ACTIVE else 'OFF'}.**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Monitor Private Messages
    # ======================
    @client.on(events.NewMessage(incoming=True))
    async def monitor_pm(event):
        if not ANTI_PM_ACTIVE:
            return
        if event.is_private and event.sender_id != OWNER_ID:
            user_id = event.sender_id

            # Update warning count
            USER_WARNINGS[user_id] = USER_WARNINGS.get(user_id, 0) + 1
            warnings_left = MAX_WARNINGS - USER_WARNINGS[user_id]

            if USER_WARNINGS[user_id] < MAX_WARNINGS:
                warning_msg = (
                    f"⚠ **Warning!**\n\n"
                    f"You are not approved to DM the owner.\n"
                    f"Warnings left before mute: `{warnings_left}`"
                )
                await event.respond(warning_msg)
            else:
                try:
                    await client.edit_permissions(event.chat_id, send_messages=False)
                except Exception:
                    pass
                await event.respond("🚫 **You have been muted due to repeated DMs.**")
