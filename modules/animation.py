import asyncio
from telethon import events
from config import OWNER_ID


def register(client):
    # ======================
    # Utility: Run animation
    # ======================
    async def run_animation(event, frames, delay=0.3):
        for frame in frames:
            await event.edit(frame)
            await asyncio.sleep(delay)

    # ======================
    # Moon phases animation
    # ======================
    @client.on(events.NewMessage(pattern=r"\.moon"))
    async def moon_animation(event):
        if event.sender_id != OWNER_ID:
            return
        frames = [
            "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘", "🌑"
        ]
        await run_animation(event, frames, 0.4)

    # ======================
    # Heartbeat animation
    # ======================
    @client.on(events.NewMessage(pattern=r"\.heart"))
    async def heart_animation(event):
        if event.sender_id != OWNER_ID:
            return
        frames = [
            "💓", "💗", "💖", "💘", "💝", "💘", "💖", "💗", "💓"
        ]
        await run_animation(event, frames, 0.3)

    # ======================
    # Loader animation
    # ======================
    @client.on(events.NewMessage(pattern=r"\.load"))
    async def loading_animation(event):
        if event.sender_id != OWNER_ID:
            return
        frames = [
            "▱▱▱▱▱",
            "▰▱▱▱▱",
            "▰▰▱▱▱",
            "▰▰▰▱▱",
            "▰▰▰▰▱",
            "▰▰▰▰▰",
            "▰▰▰▰▱",
            "▰▰▰▱▱",
            "▰▰▱▱▱",
            "▰▱▱▱▱",
            "▱▱▱▱▱",
        ]
        await run_animation(event, frames, 0.2)

    # ======================
    # 37 More Fun Animations
    # ======================
    animations = {
        "fire": ["🔥", "♨️", "🔥", "♨️", "🔥"],
        "clock": ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"],
        "earth": ["🌍", "🌎", "🌏", "🌍", "🌎", "🌏"],
        "snake": ["🐍", "🐍🐍", "🐍🐍🐍", "🐍🐍", "🐍"],
        "rocket": ["🚀", "🛸", "🛰", "🚀", "🛸"],
        "dots": ["⠁", "⠂", "⠄", "⡀", "⠄", "⠂", "⠁"],
        "wave": ["🌊", "🌊🌊", "🌊🌊🌊", "🌊🌊", "🌊"],
        "money": ["💰", "💸", "💵", "💳", "💰"],
        "happy": ["😀", "😃", "😄", "😁", "😆", "😀"],
        "angry": ["😡", "😠", "🤬", "😡"],
        "robot": ["🤖", "👾", "🤖", "👾"],
        "loading2": ["🔄", "🔁", "🔂", "🔄"],
        "stars": ["⭐", "🌟", "✨", "🌟", "⭐"],
        "bomb": ["💣", "💥", "💣", "💥"],
        "cat": ["🐱", "😺", "😸", "😹", "🐱"],
        "ghost": ["👻", "💀", "☠️", "👻"],
        "train": ["🚂", "🚆", "🚄", "🚅", "🚇"],
        "car": ["🚗", "🚕", "🚙", "🚗"],
        "snow": ["❄️", "☃️", "❄️", "☃️"],
        "eyes": ["👀", "👁", "👀", "👁"],
        "lock": ["🔒", "🔓", "🔒", "🔓"],
        "phone": ["📱", "☎️", "📱", "☎️"],
        "tv": ["📺", "📻", "📺"],
        "battery": ["🔋", "🔌", "🔋", "🔌"],
        "coffee": ["☕", "🍵", "☕", "🍵"],
        "kiss": ["😘", "😗", "😚", "😘"],
        "ball": ["⚽", "🏀", "🏈", "⚾", "🎾", "⚽"],
        "fruit": ["🍎", "🍌", "🍉", "🍇", "🍎"],
        "game": ["🎮", "🕹", "🎮", "🕹"],
        "plane": ["🛫", "🛬", "✈️", "🛫", "🛬"],
        "book": ["📖", "📕", "📗", "📘", "📙"],
        "light": ["💡", "🔦", "💡", "🔦"],
        "key": ["🔑", "🗝", "🔑", "🗝"],
        "pen": ["✒️", "🖊️", "✒️", "🖊️"],
        "flower": ["🌹", "🌻", "🌷", "🌸", "🌼", "🌹"],
        "drink": ["🍺", "🍷", "🥂", "🍺"],
        "moon2": ["🌑", "🌘", "🌗", "🌖", "🌕", "🌔", "🌓", "🌒"],
        "rainbow": ["🌈", "☀️", "🌧", "🌈"],
        "wind": ["💨", "🌬", "💨", "🌬"],
        "check": ["☑️", "✅", "✔️", "☑️"],
    }

    for name, frames in animations.items():
        async def make_anim(event, frames=frames):
            if event.sender_id != OWNER_ID:
                return
            await run_animation(event, frames, 0.3)

        client.on(events.NewMessage(pattern=fr"\.{name}"))(make_anim)
