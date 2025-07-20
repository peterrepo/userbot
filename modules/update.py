import os
import subprocess
from telethon import events
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

    @client.on(events.NewMessage(pattern=r"^\.update$"))
    @is_owner
    async def update_bot(event):
        """Pulls the latest code from Git and restarts the bot."""
        await event.edit("⏳ **Checking for updates...**")

        try:
            # Git pull to fetch latest changes
            process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                return await event.edit(f"❌ Update failed:\n`{stderr.decode()}`")

            output = stdout.decode().strip()
            if "Already up to date." in output:
                return await event.edit("✅ **Already up-to-date!**")
            else:
                await event.edit("✅ **Update successful! Restarting bot...**")
                os.execl(sys.executable, sys.executable, *sys.argv)  # Restart script
        except Exception as e:
            await event.edit(f"❌ Error during update: {e}")
