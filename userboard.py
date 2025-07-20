import os
import asyncio
import importlib
from telethon import TelegramClient, events

# ========== CONFIG ==========
API_ID = 28289547
API_HASH = "fb26885f55aad0acbda5ac7f3adf60f6"
OWNER_ID = 7292202061
SESSION_NAME = "userbot87"  # session file name
# ============================

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# ========== OWNER CHECK ==========
def is_owner(sender_id):
    return sender_id == OWNER_ID


# ========== AUTO DELETE DECORATOR ==========
async def respond_and_delete(event, message):
    reply = await event.respond(message)
    await asyncio.sleep(0.5)
    await reply.delete()
    await event.delete()


# ========== BASIC COMMANDS ==========
@client.on(events.NewMessage(pattern=r"\.ping"))
async def ping(event):
    if not is_owner(event.sender_id):
        return
    await respond_and_delete(event, "Pong!")


@client.on(events.NewMessage(pattern=r"\.alive"))
async def alive(event):
    if not is_owner(event.sender_id):
        return
    await respond_and_delete(event, "✅ UserBot is alive and running!")


# ========== DYNAMIC MODULE LOADER ==========
def load_modules():
    modules_dir = os.path.join(os.getcwd(), "modules")
    if not os.path.exists(modules_dir):
        print("No modules directory found.")
        return

    modules = [m.replace(".py", "") for m in os.listdir(modules_dir) if m.endswith(".py")]

    print(f"Found modules: {modules}")
    for module_name in modules:
        try:
            mod = importlib.import_module(f"modules.{module_name}")
            if hasattr(mod, "register"):
                mod.register(client)
            print(f"✅ Loaded module: {module_name}")
        except Exception as e:
            print(f"❌ Failed to load {module_name}: {e}")


# ========== MAIN ==========
async def main():
    print("🔄 Starting UserBot...")
    await client.start()
    print("🔐 Logged in successfully!")

    load_modules()
    print("📦 All modules loaded (skipped errors).")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
