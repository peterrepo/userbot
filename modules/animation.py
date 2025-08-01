import asyncio
from telethon import events
from config import OWNER_ID


def register(client):
    # ======================
    # Utility: Run animation
    # ======================
    async def run_animation(event, frames, delay=1):
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
            "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘", "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘" "🌑🌒🌓🌔🌕🌖🌗🌘"
        ]
        await run_animation(event, frames, 0.2)

    # ======================
    # Heartbeat animation
    # ======================
    @client.on(events.NewMessage(pattern=r"\.love"))
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
    "moon2": [
        "🌕🌖🌗🌘🌑🌒🌓🌔",
        "🌖🌗🌘🌑🌒🌓🌔🌕",
        "🌗🌘🌑🌒🌓🌔🌕🌖",
        "🌘🌑🌒🌓🌔🌕🌖🌗",
        "🌑🌒🌓🌔🌕🌖🌗🌘",
        "🌒🌓🌔🌕🌖🌗🌘🌑",
        "🌓🌔🌕🌖🌗🌘🌑🌒",
        "🌔🌕🌖🌗🌘🌑🌒🌓",
    ],

    "hearts": [
        "❤️🧡💛💚💙💜🖤🤍","🧡💛💚💙💜🖤🤍❤️","💛💚💙💜🖤🤍❤️🧡","💚💙💜🖤🤍❤️🧡💛","💙💜🖤🤍❤️🧡💛💚","💜🖤🤍❤️🧡💛💚💙","🖤🤍❤️🧡💛💚💙💜","🤍❤️🧡💛💚💙💜🖤",
    ],

    "stars": [
        "✨   ✨   ✨","  ✨   ✨   ✨","    ✨   ✨   ✨","  ✨   ✨   ✨","✨   ✨   ✨",
    ],

    "fire": [
        "🔥🔥🔥🔥🔥","🔥✨🔥✨🔥","✨🔥✨🔥✨","🔥✨🔥✨🔥","🔥🔥🔥🔥🔥",
    ],

    "loading": [
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]",
    ],

    "snake": [
         " 🐍","  🐍.   ","   🐍  .","    🐍. ","     🐍.","    🐍. ","   🐍  .","  🐍   ."," 🐍   . ",
    ],

    "rocket": [
        "🚀      ",
        "🚀💨     ",
        "🚀💨💨    ",
        "🚀💨💨💨   ",
        "🚀💨💨    ",
        "🚀💨     ",
        "🚀      ",
    ],

    "rain": [
        "☁️☁️☁️☁️\n💧💧💧💧",
        "☁️☁️☁️☁️\n  💧💧💧",
        "☁️☁️☁️☁️\n    💧💧",
        "☁️☁️☁️☁️\n      💧",
        "☁️☁️☁️☁️\n    💧💧",
        "☁️☁️☁️☁️\n  💧💧💧",
    ],

    "snow": [
        "❄️ ☃️❄️ ☃️❄️" ,"☃️❄️ ☃️❄️ ☃️❄️","☃️❄️ ☃️❄️ ☃️❄️","☃️❄️ ☃️❄️ ☃️❄️","❄️ ☃️❄️ ☃️❄️",
    ],

    "sparkle": [
        "✨✨✨✨✨","  ✨✨✨","    ✨","  ✨✨✨","✨✨✨✨✨",
    ],

    "matrix": [
        "`0101010101`",
        "`1010101010`",
        "`0101010101`",
        "`1010101010`",
    ],

    "train": [
        "🚂🚃🚃🚃      ",
        "  🚂🚃🚃🚃    ",
        "    🚂🚃🚃🚃  ",
        "      🚂🚃🚃🚃",
        "    🚂🚃🚃🚃  ",
        "  🚂🚃🚃🚃    ",
        "🚂🚃🚃🚃      ",
    ],

    "typing": [
        "`Typing.`",
        "`Typing..`",
        "`Typing...`",
        "`Typing....`",
        "`Typing.....`",
        "`Typing......`",
    ],

    "ghost": [
        "👻",
        "👻 Boo!",
        "👻👻 Boo!!",
        "👻👻👻 Boo!!!",
        "👻",
    ],

    "boom": [
        "💣",
        "💣💥",
        "💥🔥",
        "🔥✨",
        "✨💨",
        "💨",
    ],

    "wave": [
        "🌊        ",
        "🌊🌊      ",
        "🌊🌊🌊    ",
        "🌊🌊🌊🌊  ",
        "🌊🌊🌊🌊🌊.",
        "🌊🌊🌊🌊  ",
        "🌊🌊🌊   ",
        "🌊🌊      ",
        "🌊        ",
    ],

    "arrows": [
        "➡️➡️➡️➡️",
        "➡️➡️➡️",
        "➡️➡️",
        "➡️",
        "➡️➡️",
        "➡️➡️➡️",
        "➡️➡️➡️➡️",
    ],

    "flower": [
        "🌸🌼🌻🌹",
        "🌼🌻🌹🌸",
        "🌻🌹🌸🌼",
        "🌹🌸🌼🌻",
    ],

    "robot": [
        "🤖",
        "`Beep`",
        "`Boop`",
        "`Beep Boop`",
        "🤖",
    ],

    "cube": [
        "⬛⬛⬛",
        "⬛⬛",
        "⬛",
        "⬛⬛",
        "⬛⬛⬛",
    ],

    "money": [
        "💰💰💰",
        "  💰💰",
        "    💰",
        "  💰💰",
        "💰💰💰",
    ],

    "starwave": [
        "⭐    ",
        "⭐⭐  ",
        "⭐⭐⭐.",
        "⭐⭐  ",
        "⭐    ",
    ],

    "happy": [
        "😃😄😁😆",
        "😄😁😆😃",
        "😁😆😃😄",
        "😆😃😄😁",
    ],

    "angry": [
        "😡😠🤬",
        "😠🤬😡",
        "🤬😡😠",
    ],

    "spark": [
        "⚡⚡⚡",
        "⚡  ⚡",
        "⚡⚡⚡",
    ],

    "infinite": [
        "∞       ",
        "  ∞     ",
        "    ∞   ",
        "      ∞ ",
        "    ∞   ",
        "  ∞     ",
        "∞       ",
    ],

    "dots": [
        "● ○ ○ ○ ○",
        "○ ● ○ ○ ○",
        "○ ○ ● ○ ○",
        "○ ○ ○ ● ○",
        "○ ○ ○ ○ ●",
        "○ ○ ○ ● ○",
        "○ ○ ● ○ ○",
        "○ ● ○ ○ ○",
    ],

    "earth": [
        "🌍🌎🌏🌍🌎🌏",
        "🌎🌏🌍🌎🌏🌍",
        "🌏🌍🌎🌏🌍🌎",
    ],

    "clocks": [
        "🕛🕐🕑🕒",
        "🕐🕑🕒🕓",
        "🕑🕒🕓🕔",
        "🕒🕓🕔🕕",
        "🕓🕔🕕🕖",
        "🕔🕕🕖🕗",
    ],

    "meteor": [
        "☄️ .   ",
        "  ☄️ . ",
        "    ☄️.",
        "  ☄️ . ",
        "☄️ .   ",
    ],

    "ball": [
        "⚽.        ",
        "  ⚽.      ",
        "    ⚽.    ",
        "      ⚽.  ",
        "        ⚽.",
        "      ⚽.  ",
        "    ⚽.    ",
        "  ⚽.      ",
        "⚽.        ",
    ],

    # NEW 10 SUPER COOL ANIMATIONS
    "cyber": [
        "`█▒▒▒▒▒▒▒▒▒▒▒▒`",
        "`███▒▒▒▒▒▒▒▒▒▒`",
        "`█████▒▒▒▒▒▒▒▒`",
        "`███████▒▒▒▒▒▒`",
        "`█████████▒▒▒▒`",
        "`███████████▒▒`",
        "`█████████████`",
    ],

    "racecar": [
        "🏎️💨        ",
        "...🏎️💨      ",
        ".....🏎️💨    ",
        ".......🏎️💨  ",
        ".........🏎️💨",
    ],

    "glitch": [
        "`GL1TCH`",
        "`GL!TCH`",
        "`GL1T(H`",
        "`GLITCH`",
    ],

    "explosion": [
        "💣",
        "💥💥💥",
        "🔥🔥🔥🔥",
        "✨✨✨✨✨",
        "💨💨",
    ],

    "ufo": [
        "🛸...        ",
        "  .🛸..     ",
        "    ..🛸.    ",
        "      ...🛸  ",
        "        ..🛸.",
    ],

    "pulse": [
        "🔴",
        "🟠",
        "🟡",
        "🟢",
        "🔵",
        "🟣",
    ],

    "bars": [
        "▁ ▂ ▃ ▄ ▅ ▆ ▇ █",
        "█ ▇ ▆ ▅ ▄ ▃ ▂ ▁",
    ],

    "hack": [
        "`HACKING.`",
        "`HACKING..`",
        "`HACKING...`",
        "`HACKING....`",
        "`ACCESS GRANTED!`",
    ],

    "alien": [
        "👽",
        "👽👽",
        "👽👽👽",
        "👽👽",
        "👽",
    ],

    "glow": [
        "🔆",
        "🔅",
        "🔆",
        "🔅",
        "🔆",
    ],
}
    for name, frames in animations.items():
        async def make_anim(event, frames=frames):
            if event.sender_id != OWNER_ID:
                return
            await run_animation(event, frames, 0.1)

        client.on(events.NewMessage(pattern=fr"\.{name}"))(make_anim)
