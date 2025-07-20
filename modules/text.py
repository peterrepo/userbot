from telethon import events
from config import OWNER_ID

# Fancy fonts mapping for `.fancy` command
FANCY_MAP = str.maketrans(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏"
    "𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵"
)

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
    # Uppercase
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.upper (.+)"))
    @is_owner
    async def to_upper(event):
        text = event.pattern_match.group(1)
        await event.edit(text.upper())

    # -------------------
    # Lowercase
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.lower (.+)"))
    @is_owner
    async def to_lower(event):
        text = event.pattern_match.group(1)
        await event.edit(text.lower())

    # -------------------
    # Reverse
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.reverse (.+)"))
    @is_owner
    async def reverse_text(event):
        text = event.pattern_match.group(1)
        await event.edit(text[::-1])

    # -------------------
    # Fancy
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.fancy (.+)"))
    @is_owner
    async def fancy_text(event):
        text = event.pattern_match.group(1)
        fancy = text.translate(FANCY_MAP)
        await event.edit(fancy)
