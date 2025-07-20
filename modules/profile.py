import os
from telethon import events, functions
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
    # Set First Name
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.setname (.+)"))
    @is_owner
    async def set_name(event):
        new_name = event.pattern_match.group(1)
        await event.edit(f"✏️ Changing name to **{new_name}**...")
        try:
            await client(functions.account.UpdateProfileRequest(first_name=new_name))
            await event.edit(f"✅ Name changed to **{new_name}**.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Set Bio
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.setbio (.+)"))
    @is_owner
    async def set_bio(event):
        new_bio = event.pattern_match.group(1)
        await event.edit("✏️ Updating bio...")
        try:
            await client(functions.account.UpdateProfileRequest(about=new_bio))
            await event.edit(f"✅ Bio updated to:\n{new_bio}")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Set Username
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.setusername (.+)"))
    @is_owner
    async def set_username(event):
        new_username = event.pattern_match.group(1)
        await event.edit(f"✏️ Changing username to **{new_username}**...")
        try:
            await client(functions.account.UpdateUsernameRequest(new_username))
            await event.edit(f"✅ Username changed to @{new_username}.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Set Profile Picture
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.setpfp$"))
    @is_owner
    async def set_profile_pic(event):
        reply = await event.get_reply_message()
        if not reply or not reply.media:
            return await event.edit("❌ Reply to an image to set as profile picture.")

        await event.edit("🖼 Setting profile picture...")
        try:
            photo = await reply.download_media()
            await client(functions.photos.UploadProfilePhotoRequest(file=photo))
            os.remove(photo)
            await event.edit("✅ Profile picture updated.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")

    # -------------------
    # Remove Profile Picture
    # -------------------
    @client.on(events.NewMessage(pattern=r"^\.delpfp$"))
    @is_owner
    async def remove_profile_pic(event):
        await event.edit("🗑 Removing profile picture...")
        try:
            photos = await client.get_profile_photos("me")
            if not photos:
                return await event.edit("❌ No profile pictures found.")
            await client(functions.photos.DeletePhotosRequest(id=photos[:1]))
            await event.edit("✅ Profile picture removed.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
