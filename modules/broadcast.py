import json
import os
import random
from telethon import events, Button
from config import OWNER_ID

CHATS_FILE = os.path.join(os.path.dirname(__file__), "../data/chats.json")

# ======================
# JSON File Handling
# ======================
def ensure_file():
    if not os.path.exists(CHATS_FILE):
        with open(CHATS_FILE, "w") as f:
            json.dump([], f)

def load_chats():
    ensure_file()
    with open(CHATS_FILE, "r") as f:
        return json.load(f)

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f, indent=2)

# ======================
# Register Function
# ======================
def register(client):

    # ========== GET ALL CHATS ==========
    @client.on(events.NewMessage(pattern=r"^\.getchats$"))
    async def get_discussion_chats(event):
        if event.sender_id != OWNER_ID:
            return

        dialogs = await client.get_dialogs()
        chats = []
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                chats.append({
                    "id": dialog.id,
                    "name": dialog.name
                })

        save_chats(chats)
        await event.respond(f"✅ **Fetched and saved {len(chats)} chats.**")

    # ========== SHOW SAVED CHATS ==========
    @client.on(events.NewMessage(pattern=r"^\.showchats$"))
    async def show_chats(event):
        if event.sender_id != OWNER_ID:
            return

        chats = load_chats()
        if not chats:
            await event.respond("⚠️ **No saved chats found. Use `.getchats` first.**")
            return

        message = "**📋 Saved Chats:**\n\n"
        for chat in chats:
            line = f"• **{chat['name']}** (`{chat['id']}`)\n"
            if len(message) + len(line) > 4000:  # Telegram character limit
                await event.respond(message)
                message = ""
            message += line

        if message:
            await event.respond(message)

    # ========== BROADCAST TO SELECTED CHATS ==========
    @client.on(events.NewMessage(pattern=r"^\.rbroadcast (.+)$"))
    async def broadcast(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.pattern_match.group(1).split(" ", 1)
        if len(args) < 2:
            await event.respond("❌ **Usage:** `.rbroadcast <chat_ids> <message>`")
            return

        chat_ids = args[0].split(",")
        message = args[1]

        success = 0
        failed = 0
        for chat_id in chat_ids:
            try:
                await client.send_message(int(chat_id), message)
                success += 1
            except Exception:
                failed += 1

        await event.respond(f"📢 **Broadcast done!**\n✅ Success: {success}\n❌ Failed: {failed}")

    # ========== RPS GAME ==========
    active_rps = {}

    @client.on(events.NewMessage(pattern=r"^\.rps$"))
    async def rps_game(event):
        if event.sender_id != OWNER_ID or not event.is_reply:
            return

        reply = await event.get_reply_message()
        target_id = reply.sender_id

        # Create game session
        active_rps[event.chat_id] = {"owner": None, "target": None, "target_id": target_id}

        buttons = [
            [Button.inline("🪨 Rock", data=b"rock"), Button.inline("📄 Paper", data=b"paper"), Button.inline("✂️ Scissors", data=b"scissors")]
        ]

        await event.respond(
            "🎮 **Rock-Paper-Scissors Game!**\nOwner and the replied user can choose.",
            buttons=buttons
        )

    @client.on(events.CallbackQuery)
    async def handle_rps_click(event):
        if event.chat_id not in active_rps:
            return

        session = active_rps[event.chat_id]
        player = "owner" if event.sender_id == OWNER_ID else "target" if event.sender_id == session["target_id"] else None
        if not player:
            await event.answer("You're not part of this game!", alert=True)
            return

        choice = event.data.decode("utf-8")
        session[player] = choice
        await event.answer(f"You chose {choice.capitalize()}")

        # Check if both played
        if session["owner"] and session["target"]:
            result = determine_winner(session["owner"], session["target"])
            await event.edit(f"**Game Result:**\nOwner: {session['owner']}\nTarget: {session['target']}\n\n**Winner:** {result}")
            del active_rps[event.chat_id]

# ======================
# Determine RPS Winner
# ======================
def determine_winner(owner_choice, target_choice):
    if owner_choice == target_choice:
        return "Draw!"
    wins = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
    return "Owner" if wins[owner_choice] == target_choice else "Target"
