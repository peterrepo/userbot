from telethon import events, functions, types
from config import OWNER_ID

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
    # React to a Message
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.react (.+)"))
    @is_owner
    async def react_message(event):
        emoji = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a message to react.")

        await event.edit(f"😎 Adding reaction `{emoji}`...")
        try:
            await client(functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=reply.id,
                reaction=[types.ReactionEmoji(emoticon=emoji)]
            ))
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Remove Reactions
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.unreact$"))
    @is_owner
    async def remove_reaction(event):
        reply = await event.get_reply_message()
        if not reply:
            return await event.edit("❌ Reply to a message to remove reactions.")

        await event.edit("🧹 Removing reactions...")
        try:
            await client(functions.messages.SendReactionRequest(
                peer=event.chat_id,
                msg_id=reply.id,
                reaction=[]
            ))
            await event.delete()
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
