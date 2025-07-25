# clone.py - Final Fixed Clone Module by peter parker
# Commands:
#   .clone @username OR reply to a user
#   .revert - Restore your original profile

import os
from telethon import events
from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

# Globals to save your OG identity
ORIGINAL_NAME = None
ORIGINAL_BIO = None
ORIGINAL_PIC_PATH = "original_profile_pic.jpg"

def register(client):

    @client.on(events.NewMessage(pattern=r"^\.clone(?: |$)(.*)"))
    async def clone_user(event):
        global ORIGINAL_NAME, ORIGINAL_BIO

        await event.respond("🔄 **Cloning user profile... Please wait...**")

        # Save your current name, bio and profile pic (only once)
        if not ORIGINAL_NAME or not ORIGINAL_BIO:
            me = await client.get_me()
            full_me = await client(GetFullUserRequest(me.id))
            ORIGINAL_NAME = me.first_name or "User"
            ORIGINAL_BIO = full_me.full_user.about or ""
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
            await event.respond(f"❌ Couldn't fetch user: `{e}`")
            return

        target = user.users[0]
        full_target = user.full_user

        # Extract name & bio
        name = target.first_name or "Unknown"
        bio = full_target.about or ""

        # Update your profile name & bio
        try:
            await client(functions.account.UpdateProfileRequest(first_name=name, about=bio))
        except Exception as e:
            await event.respond(f"⚠ Failed to update name/bio: `{e}`")
            return

        # Clone profile picture
        try:
            photo_path = await client.download_profile_photo(target.id, "cloned_pic.jpg")
            if photo_path:
                await client(functions.photos.UploadProfilePhotoRequest(file=photo_path))
                await event.respond(f"✅ **𝐍𝐎𝐖 𝐈 𝐀𝐌 {name}** 😈")
            else:
                await event.respond("⚠ **Cloned name & bio, but target has no profile photo.**")
        except Exception as e:
            await event.respond(f"⚠ Cloned name & bio, but failed to clone photo: `{e}`")

    @client.on(events.NewMessage(pattern=r"^\.revert$"))
    async def revert_profile(event):
        global ORIGINAL_NAME, ORIGINAL_BIO

        await event.respond("🔄 𝐂𝐎𝐌𝐈𝐍𝐆 𝐁𝐀𝐂𝐊 𝐈𝐍 𝐅𝐎𝐑𝐌 🔥...")

        try:
            if ORIGINAL_NAME:
                await client(functions.account.UpdateProfileRequest(first_name=ORIGINAL_NAME))
            if ORIGINAL_BIO:
                await client(functions.account.UpdateProfileRequest(about=ORIGINAL_BIO))
        except Exception as e:
            await event.respond(f"⚠ Failed to restore name/bio: `{e}`")

        # Restore profile photo
        if os.path.exists(ORIGINAL_PIC_PATH):
            try:
                await client(functions.photos.UploadProfilePhotoRequest(file=ORIGINAL_PIC_PATH))
            except Exception as e:
                await event.respond(f"⚠ Failed to restore photo: `{e}`")

        # Optional: Clean up the cloned pic file
        if os.path.exists("cloned_pic.jpg"):
            os.remove("cloned_pic.jpg")

        await event.respond("✅ **𝐁𝐀𝐂𝐊 𝐈𝐍 𝐅𝐎𝐑𝐌 🗿**")
