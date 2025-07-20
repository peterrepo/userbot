import asyncio
from telethon import events
from config import OWNER_ID
import random

EMOJI_LIST = ['😀', '😂', '😍', '🥳', '😎', '🤩', '🔥', '💀', '👻', '🦄', '🐍', '🍕', '⚡', '🎉', '🚀']

def text_to_emoji(text):
    """Replace each character with a random emoji or itself."""
    return ''.join(random.choice(EMOJI_LIST) if c != ' ' else ' ' for c in text)

def repeat_emoji(text, count=5):
    """Repeat the text as emoji pattern."""
    emoji = random.choice(EMOJI_LIST)
    return ' '.join([emoji + text + emoji for _ in range(count)])

def register(client):
    @client.on(events.NewMessage(pattern=r"\.emojiart"))
    async def emoji_art(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.raw_text.split(" ", 1)
        if len(args) < 2:
            await event.reply("**Usage:** `.emojiart <text>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        text = args[1]
        emoji_text = text_to_emoji(text)
        await event.reply(f"🎨 **Emoji Art:**\n{emoji_text}")
        await asyncio.sleep(0.5)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.emojispam"))
    async def emoji_spam(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.raw_text.split(" ", 2)
        if len(args) < 3:
            await event.reply("**Usage:** `.emojispam <count> <text>`")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        try:
            count = int(args[1])
        except ValueError:
            await event.reply("⚠ **Count must be a number!**")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        text = args[2]
        pattern = repeat_emoji(text, count)
        await event.reply(f"💥 **Emoji Spam:**\n{pattern}")
        await asyncio.sleep(0.5)
        await event.delete()

    @client.on(events.NewMessage(pattern=r"\.randomemoji"))
    async def random_emoji(event):
        if event.sender_id != OWNER_ID:
            return

        random_emojis = ' '.join(random.choices(EMOJI_LIST, k=10))
        await event.reply(f"🎲 **Random Emojis:**\n{random_emojis}")
        await asyncio.sleep(0.5)
        await event.delete()
