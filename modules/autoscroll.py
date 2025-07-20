import asyncio
from telethon import events
from config import OWNER_ID

AUTOSCROLL_ACTIVE = False
AUTOSCROLL_INTERVAL = 5  # Default interval (seconds)
AUTOSCROLL_TEXT = "This is the default autoscroll message."


def register(client):
    # ======================
    # Toggle Autoscroll
    # ======================
    @client.on(events.NewMessage(pattern=r"\.autoscroll (on|off)$"))
    async def toggle_autoscroll(event):
        global AUTOSCROLL_ACTIVE
        if event.sender_id != OWNER_ID:
            return

        state = event.pattern_match.group(1).lower()
        AUTOSCROLL_ACTIVE = state == "on"

        if AUTOSCROLL_ACTIVE:
            await event.edit("**Autoscroll is now ON.**")
            client.loop.create_task(run_autoscroll(client, event.chat_id))
        else:
            await event.edit("**Autoscroll is now OFF.**")

        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Set Interval
    # ======================
    @client.on(events.NewMessage(pattern=r"\.autoscrollinterval (\d+)$"))
    async def set_interval(event):
        global AUTOSCROLL_INTERVAL
        if event.sender_id != OWNER_ID:
            return

        AUTOSCROLL_INTERVAL = int(event.pattern_match.group(1))
        await event.edit(f"**Autoscroll interval set to {AUTOSCROLL_INTERVAL} seconds.**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Set Message
    # ======================
    @client.on(events.NewMessage(pattern=r"\.autoscrollmsg (.+)$"))
    async def set_message(event):
        global AUTOSCROLL_TEXT
        if event.sender_id != OWNER_ID:
            return

        AUTOSCROLL_TEXT = event.pattern_match.group(1)
        await event.edit(f"**Autoscroll message updated to:** `{AUTOSCROLL_TEXT}`")
        await asyncio.sleep(0.5)
        await event.delete()


async def run_autoscroll(client, chat_id):
    global AUTOSCROLL_ACTIVE
    while AUTOSCROLL_ACTIVE:
        try:
            await client.send_message(chat_id, AUTOSCROLL_TEXT)
            await asyncio.sleep(AUTOSCROLL_INTERVAL)
        except Exception as e:
            print(f"[Autoscroll] Error: {e}")
            await asyncio.sleep(AUTOSCROLL_INTERVAL)
