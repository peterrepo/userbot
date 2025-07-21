import json
import os
from telethon import events, functions

# Path to Anti-PM data file
DATA_DIR = "userbot/data"
DATA_FILE = os.path.join(DATA_DIR, "anti-pm-me.json")

os.makedirs(DATA_DIR, exist_ok=True)

# Load and save JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        data = {"enabled": True, "whitelist": [], "blacklist": [], "warnings": {}}
        save_data(data)
    else:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def register(client):

    # Helper to get target user
    async def get_target_user(event):
        if event.is_reply:
            msg = await event.get_reply_message()
            user = await msg.get_sender()
        else:
            user = await event.get_sender()
        return user

    # Toggle Anti-PM ON/OFF
    @client.on(events.NewMessage(pattern=r"\.antipm (on|off)$"))
    async def toggle_antipm(event):
        mode = event.pattern_match.group(1).lower()
        data["enabled"] = (mode == "on")
        save_data(data)
        await event.respond(f"**Anti-PM is now {'ON' if data['enabled'] else 'OFF'}**")

    # Add user to whitelist
    @client.on(events.NewMessage(pattern=r"\.addwl$"))
    async def add_whitelist(event):
        user = await get_target_user(event)
        if user.id not in data["whitelist"]:
            data["whitelist"].append(user.id)
            save_data(data)
            await event.respond(f"**Added {user.first_name} to whitelist.**")
        else:
            await event.respond("**User is already in whitelist.**")

    # Remove user from whitelist
    @client.on(events.NewMessage(pattern=r"\.rmwl$"))
    async def remove_whitelist(event):
        user = await get_target_user(event)
        if user.id in data["whitelist"]:
            data["whitelist"].remove(user.id)
            save_data(data)
            await event.respond(f"**Removed {user.first_name} from whitelist.**")
        else:
            await event.respond("**User is not in whitelist.**")

    # Show whitelist
    @client.on(events.NewMessage(pattern=r"\.showwl$"))
    async def show_whitelist(event):
        if not data["whitelist"]:
            await event.respond("**Whitelist is empty.**")
            return
        msg = "**Whitelisted Users:**\n"
        for uid in data["whitelist"]:
            msg += f"- `{uid}`\n"
        await event.respond(msg)

    # Add user to blacklist
    @client.on(events.NewMessage(pattern=r"\.addbl$"))
    async def add_blacklist(event):
        user = await get_target_user(event)
        if user.id not in data["blacklist"]:
            data["blacklist"].append(user.id)
            save_data(data)
            await event.respond(f"**Added {user.first_name} to blacklist.**")
        else:
            await event.respond("**User is already in blacklist.**")

    # Remove user from blacklist
    @client.on(events.NewMessage(pattern=r"\.rmbl$"))
    async def remove_blacklist(event):
        user = await get_target_user(event)
        if user.id in data["blacklist"]:
            data["blacklist"].remove(user.id)
            save_data(data)
            await event.respond(f"**Removed {user.first_name} from blacklist.**")
        else:
            await event.respond("**User is not in blacklist.**")

    # Show blacklist
    @client.on(events.NewMessage(pattern=r"\.showbl$"))
    async def show_blacklist(event):
        if not data["blacklist"]:
            await event.respond("**Blacklist is empty.**")
            return
        msg = "**Blacklisted Users:**\n"
        for uid in data["blacklist"]:
            msg += f"- `{uid}`\n"
        await event.respond(msg)

    # Anti-PM logic
    @client.on(events.NewMessage(incoming=True))
    async def check_pm(event):
        if not data["enabled"] or not event.is_private:
            return

        user = await event.get_sender()
        if user.id in data["whitelist"]:
            return  # Whitelisted user
        if user.id in data["blacklist"]:
            await client(functions.contacts.BlockRequest(user.id))
            return

        warnings = data["warnings"].get(str(user.id), 0) + 1
        data["warnings"][str(user.id)] = warnings
        save_data(data)

        if warnings >= 3:
            await event.respond("**You have been blocked for spamming my DMs.**")
            await client(functions.contacts.BlockRequest(user.id))
        else:
            await event.respond(
                f"**Warning {warnings}/3:** Please do not message me without approval."
            )
