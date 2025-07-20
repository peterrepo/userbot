import os
import psutil
import time
from datetime import datetime
from telethon import events
from config import OWNER_ID

start_time = time.time()  # Bot uptime tracker

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def format_uptime(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.stats$"))
    @is_owner
    async def stats_cmd(event):
        uptime = format_uptime(time.time() - start_time)

        # CPU and memory stats
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent

        # System info
        try:
            sys_info = os.uname()
            system_name = f"{sys_info.sysname} {sys_info.release}"
        except AttributeError:
            system_name = os.name.upper()

        msg = (
            "**📊 System & Bot Stats:**\n\n"
            f"**System:** `{system_name}`\n"
            f"**CPU Usage:** `{cpu_usage}%`\n"
            f"**RAM Usage:** `{ram_usage}%`\n"
            f"**Disk Usage:** `{disk_usage}%`\n"
            f"**Uptime:** `{uptime}`\n"
        )

        await event.edit(msg)
