import asyncio
from telethon import events
from telethon.tl import functions
from config import OWNER_ID


async def clone_user(client, user):
    """Clone profile info from another user."""
    # Get user information
    full_user = await client(functions.users.GetFullUserRequest(user.id))

    # Clone profile photo
    if full_user.profile_photo:
        photo = await client.download_profile_photo(user, file=bytes)
        await client(functions.photos.UploadProfilePhotoRequest(
            file=photo
        ))

    # Clone first name, last name, and bio
    first_name = full_user.user.first_name or ""
    last_name = full_user.user.last_name or ""
    about = full_user.about or ""

    await client(functions.account.UpdateProfileRequest(
        first_name=first_name,
        last_name=last_name,
        about=about
    ))


def register(client):
    # ======================
    # Clone Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.clone$"))
    async def clone(event):
        if event.sender_id != OWNER_ID:
            return

        if not event.is_reply:
            await event.reply("**Reply to a user's message to clone their profile!**")
            await asyncio.sleep(0.5)
            await event.delete()
            return

        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()

        await event.reply(f"**Cloning {user.first_name}...**")
        await clone_user(client, user)
        await event.reply(f"**Cloned {user.first_name}'s profile successfully!**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Restore Command
    # ======================
    @client.on(events.NewMessage(pattern=r"\.restore$"))
    async def restore(event):
        if event.sender_id != OWNER_ID:
            return

        await event.reply("**Restoring your original profile...**")
        # Clear all changes (name, bio, and remove profile photos)
        await client(functions.photos.UpdateProfilePhotoRequest(
            id=0  # Remove current profile picture
        ))
        await client(functions.account.UpdateProfileRequest(
            first_name="Userbot",
            last_name="",
            about="Restored by Userbot"
        ))
        await event.reply("**Profile restored!**")
        await asyncio.sleep(0.5)
        await event.delete()

