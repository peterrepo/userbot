import os
import asyncio
import aiohttp
from telethon import events
from config import OWNER_ID

CARBON_API = "https://carbonara.solopov.dev/api/cook"  # Free Carbon API


async def create_carbon_image(code: str, output_file: str):
    """Generate a Carbon code image and save to output_file."""
    async with aiohttp.ClientSession() as session:
        async with session.post(CARBON_API, json={"code": code}) as resp:
            if resp.status == 200:
                with open(output_file, "wb") as f:
                    f.write(await resp.read())
                return output_file
            else:
                return None


def register(client):
    @client.on(events.NewMessage(pattern=r"\.carbon"))
    async def carbon_cmd(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only

        # Get code text
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            code = reply_msg.text
        else:
            parts = event.raw_text.split(" ", 1)
            if len(parts) == 1:
                await event.reply("**Usage:** `.carbon <code>` or reply to a message.")
                await asyncio.sleep(0.5)
                await event.delete()
                return
            code = parts[1]

        await event.reply("**Creating Carbon image...**")

        output_file = "carbon.png"
        result = await create_carbon_image(code, output_file)

        if result:
            await event.respond(file=output_file, message="**Here is your Carbon image:**")
            os.remove(output_file)
        else:
            await event.respond("**Failed to generate Carbon image.**")

        await asyncio.sleep(0.5)
        await event.delete()
