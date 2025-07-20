from telethon import events
from telethon.tl.functions.phone import (
    CreateGroupCallRequest,
    DiscardGroupCallRequest,
    InviteToGroupCallRequest,
    GetGroupCallRequest,
)
from telethon.tl.types import InputPeerUser
from userbot import bot

# Dictionary to track active calls per chat
active_calls = {}

@bot.on(events.NewMessage(pattern=r"^\.vcstart$"))
async def start_voice_chat(event):
    chat = await event.get_input_chat()
    try:
        result = await event.client(CreateGroupCallRequest(
            peer=chat,
            random_id=0
        ))
        active_calls[event.chat_id] = result.call
        await event.reply("🎙 **Voice Chat started!**")
    except Exception as e:
        await event.reply(f"❌ **Failed to start VC:** `{e}`")

@bot.on(events.NewMessage(pattern=r"^\.vcstop$"))
async def stop_voice_chat(event):
    if event.chat_id not in active_calls:
        await event.reply("❌ **No active voice chat found!**")
        return
    
    try:
        await event.client(DiscardGroupCallRequest(
            call=active_calls[event.chat_id]
        ))
        del active_calls[event.chat_id]
        await event.reply("🔇 **Voice Chat stopped!**")
    except Exception as e:
        await event.reply(f"❌ **Failed to stop VC:** `{e}`")

@bot.on(events.NewMessage(pattern=r"^\.vcinvite$"))
async def invite_to_voice_chat(event):
    if event.chat_id not in active_calls:
        await event.reply("❌ **Start a voice chat first!**")
        return

    try:
        participants = await event.client.get_participants(event.chat_id)
        users = [InputPeerUser(user.id, user.access_hash) for user in participants]
        await event.client(InviteToGroupCallRequest(
            call=active_calls[event.chat_id],
            users=users
        ))
        await event.reply(f"📢 **Invited {len(users)} members to the VC!**")
    except Exception as e:
        await event.reply(f"❌ **Failed to invite users:** `{e}`")

@bot.on(events.NewMessage(pattern=r"^\.vcinfo$"))
async def voice_chat_info(event):
    if event.chat_id not in active_calls:
        await event.reply("❌ **No active voice chat!**")
        return

    try:
        info = await event.client(GetGroupCallRequest(
            call=active_calls[event.chat_id]
        ))
        await event.reply(f"🎙 **VC Info:** `{info}`")
    except Exception as e:
        await event.reply(f"❌ **Failed to get VC info:** `{e}`")

