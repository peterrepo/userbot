import random
from telethon import events
from config import OWNER_ID

# Sample questions
TRUTH_QUESTIONS = [
    "What is your biggest fear?",
    "Have you ever lied to your best friend?",
    "What is your most embarrassing moment?",
    "If you could change one thing in your life, what would it be?",
    "Who was your first crush?",
]

DARE_TASKS = [
    "Send a funny meme to the group.",
    "Change your profile picture to something silly for 1 hour.",
    "Text a random emoji to 5 people.",
    "Post the last photo you took on your phone.",
    "Shout out your favorite song lyrics in the chat.",
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

    @client.on(events.NewMessage(pattern=r"^\.truth$"))
    @is_owner
    async def truth_cmd(event):
        """Send a random truth question."""
        question = random.choice(TRUTH_QUESTIONS)
        await event.edit(f"**Truth:** {question}")

    @client.on(events.NewMessage(pattern=r"^\.dare$"))
    @is_owner
    async def dare_cmd(event):
        """Send a random dare task."""
        task = random.choice(DARE_TASKS)
        await event.edit(f"**Dare:** {task}")
