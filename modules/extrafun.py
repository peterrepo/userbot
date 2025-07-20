import asyncio
import random
import json
import os
from telethon import events
from config import OWNER_ID

DATA_FILE = "data/extrafun.json"

# Ensure data file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"jokes": [], "quotes": [], "roasts": [], "insults": []}, f, indent=4)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def register(client):

    # ===== RANDOM JOKE =====
    @client.on(events.NewMessage(pattern=r"\.joke"))
    async def joke(event):
        if event.sender_id != OWNER_ID:
            return
        data = load_data()
        jokes = data.get("jokes", [])
        if not jokes:
            await event.reply("😢 No jokes found. Add one using `.add-joke <text>`")
        else:
            await event.reply(f"😂 **Joke:** {random.choice(jokes)}")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== RANDOM QUOTE =====
    @client.on(events.NewMessage(pattern=r"\.quote"))
    async def quote(event):
        if event.sender_id != OWNER_ID:
            return
        data = load_data()
        quotes = data.get("quotes", [])
        if not quotes:
            await event.reply("😢 No quotes found. Add one using `.add-quote <text>`")
        else:
            await event.reply(f"💡 **Quote:** {random.choice(quotes)}")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== RANDOM ROAST =====
    @client.on(events.NewMessage(pattern=r"\.roast"))
    async def roast(event):
        if event.sender_id != OWNER_ID:
            return
        data = load_data()
        roasts = data.get("roasts", [])
        if not roasts:
            await event.reply("😢 No roasts found. Add one using `.add-roast <text>`")
        else:
            await event.reply(f"🔥 **Roast:** {random.choice(roasts)}")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== RANDOM INSULT =====
    @client.on(events.NewMessage(pattern=r"\.insult"))
    async def insult(event):
        if event.sender_id != OWNER_ID:
            return
        data = load_data()
        insults = data.get("insults", [])
        if not insults:
            await event.reply("😢 No insults found. Add one using `.add-insult <text>`")
        else:
            await event.reply(f"😈 **Insult:** {random.choice(insults)}")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== ADD JOKE =====
    @client.on(events.NewMessage(pattern=r"\.add-joke"))
    async def add_joke(event):
        if event.sender_id != OWNER_ID:
            return
        text = event.raw_text.split(" ", 1)
        if len(text) < 2:
            await event.reply("**Usage:** `.add-joke <text>`")
        else:
            data = load_data()
            data["jokes"].append(text[1])
            save_data(data)
            await event.reply("✅ **Joke added successfully!**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== ADD QUOTE =====
    @client.on(events.NewMessage(pattern=r"\.add-quote"))
    async def add_quote(event):
        if event.sender_id != OWNER_ID:
            return
        text = event.raw_text.split(" ", 1)
        if len(text) < 2:
            await event.reply("**Usage:** `.add-quote <text>`")
        else:
            data = load_data()
            data["quotes"].append(text[1])
            save_data(data)
            await event.reply("✅ **Quote added successfully!**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== ADD ROAST =====
    @client.on(events.NewMessage(pattern=r"\.add-roast"))
    async def add_roast(event):
        if event.sender_id != OWNER_ID:
            return
        text = event.raw_text.split(" ", 1)
        if len(text) < 2:
            await event.reply("**Usage:** `.add-roast <text>`")
        else:
            data = load_data()
            data["roasts"].append(text[1])
            save_data(data)
            await event.reply("✅ **Roast added successfully!**")
        await asyncio.sleep(0.5)
        await event.delete()

    # ===== ADD INSULT =====
    @client.on(events.NewMessage(pattern=r"\.add-insult"))
    async def add_insult(event):
        if event.sender_id != OWNER_ID:
            return
        text = event.raw_text.split(" ", 1)
        if len(text) < 2:
            await event.reply("**Usage:** `.add-insult <text>`")
        else:
            data = load_data()
            data["insults"].append(text[1])
            save_data(data)
            await event.reply("✅ **Insult added successfully!**")
        await asyncio.sleep(0.5)
        await event.delete()
