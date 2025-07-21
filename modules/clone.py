# clone.py - Fixed Clone Module
# Commands:
#   .clone @username OR reply to a user
#   .revert - Restore original profile

import os
from telethon import events
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

ORIGINAL_NAME = None
ORIGINAL_PIC_PATH = "original_profile_pic.jpg"


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.clone(?: |$)(.*)"))
    async def clone_user(event):
        global ORIGINAL_NAME

        await event.respond("🔄 **Fetching user details...**")

        # Save original name and photo if not saved
        if not ORIGINAL_NAME:
            me = await client.get_me()
            ORIGINAL_NAME = me.first_name or "User"
            photos = await client.get_profile_photos("me", limit=1)
            if photos:
                await client.download_media(photos[0], ORIGINAL_PIC_PATH)

        # Identify target user
        input_arg = event.pattern_match.group(1)
        try:
            if event.is_reply and not input_arg:
                reply = await event.get_reply_message()
                user = await client(GetFullUserRequest(reply.sender_id))
            else:
                user = await client(GetFullUserRequest(input_arg))
        except Exception as e:
            await event.respond(f"❌ Failed to get user: `{e}`")
            return

        # Get target's name
        first_name = getattr(user.users, "first_name", None) or "Unknown"

        # Clone name
        await client(functions.account.UpdateProfileRequest(first_name=first_name))

        # Clone photo
        try:
            photo_path = await client.download_profile_photo(user.user.id, "cloned_pic.jpg")
            if photo_path:
                await client(functions.photos.UploadProfilePhotoRequest(file=photo_path))
                await event.respond(f"✅ **Cloned {first_name} successfully!**")
            else:
                await event.respond("⚠ **Cloned name, but target has no profile photo.**")
        except Exception as e:
            await event.respond(f"⚠ Cloned name but failed to set profile photo: `{e}`")

    @client.on(events.NewMessage(pattern=r"^\.revert$"))
    async def revert_profile(event):
        global ORIGINAL_NAME

        await event.respond("🔄 **Reverting profile...**")

        # Restore name
        if ORIGINAL_NAME:
            await client(functions.account.UpdateProfileRequest(first_name=ORIGINAL_NAME))

        # Restore photo
        if os.path.exists(ORIGINAL_PIC_PATH):
            try:
                await client(functions.photos.UploadProfilePhotoRequest(file=ORIGINAL_PIC_PATH))
            except Exception as e:
                await event.respond(f"⚠ Failed to restore photo: `{e}`")

        await event.respond("✅ **Profile reverted!**")
