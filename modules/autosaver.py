from telethon import events
from config import OWNER_ID

AUTOSAVER_ACTIVE = False


def register(client):
    # ======================
    # Toggle Autosaver
    # ======================
    @client.on(events.NewMessage(pattern=r"\.autosave (on|off)$"))
    async def toggle_autosave(event):
        global AUTOSAVER_ACTIVE
        if event.sender_id != OWNER_ID:
            return

        state = event.pattern_match.group(1).lower()
        AUTOSAVER_ACTIVE = state == "on"

        if AUTOSAVER_ACTIVE:
            await event.edit("**Autosaver is now ON.**")
        else:
            await event.edit("**Autosaver is now OFF.**")

        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Save Incoming Media
    # ======================
    @client.on(events.NewMessage(incoming=True))
    async def save_incoming(event):
        if not AUTOSAVER_ACTIVE:
            return

        try:
            if event.sender_id != OWNER_ID:  # Avoid saving own messages
                # Save only if media exists (including self-destruct)
                if event.media:
                    await client.send_message("me", f"**Saved from {event.sender_id}:**")
                    await client.forward_messages("me", event.message)
        except Exception as e:
            print(f"[Autosaver] Error: {e}")
