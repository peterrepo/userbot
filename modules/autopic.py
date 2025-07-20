import os
import asyncio
from telethon import events
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from config import OWNER_ID

AUTO_PIC_ACTIVE = False
AUTO_PIC_FOLDER = "data/autopic"  # Folder for profile pictures
AUTO_PIC_INTERVAL = 60  # Interval in seconds


def register(client):
    # ======================
    # Toggle AutoPic
    # ======================
    @client.on(events.NewMessage(pattern=r"\.autopic (on|off)$"))
    async def toggle_autopic(event):
        global AUTO_PIC_ACTIVE
        if event.sender_id != OWNER_ID:
            return

        state = event.pattern_match.group(1).lower()
        AUTO_PIC_ACTIVE = state == "on"

        if AUTO_PIC_ACTIVE:
            await event.edit("**AutoPic is now ON.**")
            client.loop.create_task(run_autopic(client))
        else:
            await event.edit("**AutoPic is now OFF.**")

        await asyncio.sleep(0.5)
        await event.delete()

    # ======================
    # Set Interval
    # ======================
    @client.on(events.NewMessage(pattern=r"\.autopicinterval (\d+)$"))
    async def set_interval(event):
        global AUTO_PIC_INTERVAL
        if event.sender_id != OWNER_ID:
            return
        AUTO_PIC_INTERVAL = int(event.pattern_match.group(1))
        await event.edit(f"**AutoPic interval set to {AUTO_PIC_INTERVAL} seconds.**")
        await asyncio.sleep(0.5)
        await event.delete()


async def run_autopic(client):
    global AUTO_PIC_ACTIVE
    while AUTO_PIC_ACTIVE:
        try:
            if not os.path.exists(AUTO_PIC_FOLDER):
                os.makedirs(AUTO_PIC_FOLDER)
            images = [f for f in os.listdir(AUTO_PIC_FOLDER) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            if not images:
                await asyncio.sleep(AUTO_PIC_INTERVAL)
                continue

            for img in images:
                if not AUTO_PIC_ACTIVE:
                    return
                path = os.path.join(AUTO_PIC_FOLDER, img)
                try:
                    await client(UploadProfilePhotoRequest(file=await client.upload_file(path)))
                except Exception as e:
                    print(f"[AutoPic] Failed to set profile photo: {e}")
                await asyncio.sleep(AUTO_PIC_INTERVAL)
        except Exception as e:
            print(f"[AutoPic] Error: {e}")
            await asyncio.sleep(AUTO_PIC_INTERVAL)
