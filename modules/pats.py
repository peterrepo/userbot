import random
from telethon import events
from config import OWNER_ID

# Local GIF/IMG lists (you can expand or load from data JSON)
PATS = [
    "https://media.tenor.com/ebVhbxA_Ae8AAAAC/anime-pat.gif",
    "https://media.tenor.com/FPyB_7ZvqJ4AAAAC/pat.gif",
]

KISSES = [
    "https://media.tenor.com/PblowV6HgKQAAAAC/anime-kiss.gif",
    "https://media.tenor.com/GEUhtF3UGyIAAAAC/kiss.gif",
]

HUGS = [
    "https://media.tenor.com/6vE6c7rZ4J4AAAAC/hug-anime.gif",
    "https://media.tenor.com/5Ha27yZpQoIAAAAC/hug-love.gif",
]

FUCKS = [
    "https://media.tenor.com/7kL9vNYY43MAAAAC/hentai-sex.gif",
    "https://media.tenor.com/jfKPVnX2gRMAAAAC/anime-hentai.gif",
]

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.pat$"))
    @is_owner
    async def pat_command(event):
        gif = random.choice(PATS)
        await client.send_file(event.chat_id, gif, caption="🤚 *Pat pat!*")
        await event.delete()

    @client.on(events.NewMessage(pattern=r"^\.kiss$"))
    @is_owner
    async def kiss_command(event):
        gif = random.choice(KISSES)
        await client.send_file(event.chat_id, gif, caption="💋 *Kiss!*")
        await event.delete()

    @client.on(events.NewMessage(pattern=r"^\.hug$"))
    @is_owner
    async def hug_command(event):
        gif = random.choice(HUGS)
        await client.send_file(event.chat_id, gif, caption="🤗 *Hug!*")
        await event.delete()

    @client.on(events.NewMessage(pattern=r"^\.fuck$"))
    @is_owner
    async def fuck_command(event):
        gif = random.choice(FUCKS)
        await client.send_file(event.chat_id, gif, caption="🔞 *NSFW!*")
        await event.delete()
