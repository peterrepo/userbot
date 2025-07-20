import asyncio
from telethon import events
from config import OWNER_ID

# States
GHOST_MODE = False
PHANTOM_DELAY = None  # None = off, otherwise number of seconds

def register(client):

    # ========== TOGGLE GHOST MODE ==========
    @client.on(events.NewMessage(pattern=r"\.ghost (on|off)"))
    async def toggle_ghost(event):
        global GHOST_MODE
        if event.sender_id != OWNER_ID:
            return

        state = event.pattern_match.group(1).lower()
        if state == "on":
            GHOST_MODE = True
            await event.respond("👻 **Ghost Mode Activated!**")
        else:
            GHOST_MODE = False
            await event.respond("👻 **Ghost Mode Deactivated!**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ========== TOGGLE PHANTOM MODE ==========
    @client.on(events.NewMessage(pattern=r"\.phantom (.+)"))
    async def toggle_phantom(event):
        global PHANTOM_DELAY
        if event.sender_id != OWNER_ID:
            return

        value = event.pattern_match.group(1).strip().lower()
        if value == "off":
            PHANTOM_DELAY = None
            await event.respond("💨 **Phantom Mode Off.**")
        else:
            try:
                delay = float(value)
                if delay <= 0:
                    raise ValueError
                PHANTOM_DELAY = delay
                await event.respond(f"💨 **Phantom Mode ON:** {delay}s delay.")
            except ValueError:
                await event.respond("❌ **Invalid delay. Use `.phantom <seconds>` or `.phantom off`.**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ========== DELETE MESSAGES IN GHOST MODE ==========
    @client.on(events.NewMessage(outgoing=True))
    async def ghost_delete(event):
        if GHOST_MODE and event.sender_id == OWNER_ID:
            await asyncio.sleep(2)
            await event.delete()

    # ========== PHANTOM AUTO DELETE ==========
    @client.on(events.NewMessage(outgoing=True))
    async def phantom_delete(event):
        if PHANTOM_DELAY and event.sender_id == OWNER_ID:
            await asyncio.sleep(PHANTOM_DELAY)
            await event.delete()

