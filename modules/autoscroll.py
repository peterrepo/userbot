import random
import asyncio
from telethon import events
from config import OWNER_ID

# ===========================
# GAMES LIST
# ===========================
GAMES = [
    "dice", "coin", "rps", "guess", "math", "word",
    "trivia", "numberrace", "emoji", "hangman",
    "typerace", "truth", "dare", "country",
    "flag", "scramble", "quiz", "animal",
    "memory", "mathrace"
]

# Predefined Data
TRIVIA_QUESTIONS = [
    ("What is the capital of France?", "paris"),
    ("Who wrote 'Harry Potter'?", "jk rowling"),
    ("Which planet is known as the Red Planet?", "mars"),
]

WORDS = ["python", "telegram", "hashira", "demon", "slayer", "anime", "manga"]

COUNTRIES = ["India", "USA", "Japan", "France", "Germany", "Brazil", "Canada"]

ANIMALS = ["lion", "tiger", "panda", "elephant", "giraffe"]

# ===========================
# REGISTER GAMES
# ===========================
def register(client):

    @client.on(events.NewMessage(pattern=r"^\.game\s+(\w+)$"))
    async def game_handler(event):
        if event.sender_id != OWNER_ID:
            return
        game_name = event.pattern_match.group(1).lower()
        if game_name not in GAMES:
            await event.reply(f"🎮 **Available Games:** {', '.join(GAMES)}")
            return

        if game_name == "dice":
            await event.reply(f"🎲 You rolled a {random.randint(1,6)}!")

        elif game_name == "coin":
            await event.reply(f"🪙 Coin toss: **{random.choice(['Heads', 'Tails'])}**")

        elif game_name == "rps":
            await event.reply(f"✊ Rock, ✋ Paper, ✌ Scissors! I choose **{random.choice(['Rock','Paper','Scissors'])}**")

        elif game_name == "guess":
            number = random.randint(1,10)
            await event.reply("🔢 Guess a number between 1-10! (Reply with your guess)")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.isdigit() and int(reply.raw_text) == number:
                await reply.reply("🎉 Correct! You guessed it!")
            else:
                await reply.reply(f"❌ Wrong! It was {number}.")

        elif game_name == "math":
            a, b = random.randint(1, 10), random.randint(1, 10)
            await event.reply(f"➕ Solve: {a} + {b} = ?")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.strip() == str(a + b):
                await reply.reply("🎉 Correct!")
            else:
                await reply.reply(f"❌ Wrong! The answer is {a + b}.")

        elif game_name == "word":
            word = random.choice(WORDS)
            scrambled = "".join(random.sample(word, len(word)))
            await event.reply(f"🔤 Unscramble this: `{scrambled}`")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.lower() == word:
                await reply.reply("🎉 Correct!")
            else:
                await reply.reply(f"❌ Wrong! The word was `{word}`.")

        elif game_name == "trivia":
            q, a = random.choice(TRIVIA_QUESTIONS)
            await event.reply(f"❓ {q}")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.lower() == a:
                await reply.reply("🎉 Correct!")
            else:
                await reply.reply(f"❌ Wrong! The answer is `{a}`.")

        elif game_name == "numberrace":
            await event.reply("🏁 First to send a number wins! GO!")
            reply = await client.wait_for(events.NewMessage)
            await reply.reply(f"🎉 {reply.sender.first_name} wins!")

        elif game_name == "emoji":
            emoji = random.choice(["😀", "😎", "🔥", "💧", "🍕", "🎵"])
            await event.reply(f"Guess the emoji: `{emoji}`")

        elif game_name == "hangman":
            word = random.choice(WORDS)
            display = ["_"] * len(word)
            attempts = 6
            await event.reply(f"🎮 Hangman: {' '.join(display)} (Attempts: {attempts})")
            while attempts > 0 and "_" in display:
                guess = await client.wait_for(events.NewMessage(from_users=event.sender_id))
                char = guess.raw_text.lower()
                if char in word:
                    for i, c in enumerate(word):
                        if c == char:
                            display[i] = char
                else:
                    attempts -= 1
                await event.reply(f"{' '.join(display)} (Attempts: {attempts})")
            if "_" not in display:
                await event.reply("🎉 You won!")
            else:
                await event.reply(f"❌ You lost! Word was `{word}`.")

        elif game_name == "typerace":
            word = random.choice(WORDS)
            await event.reply(f"⚡ Type this word as fast as you can: `{word}`")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.lower() == word:
                await reply.reply("🎉 You win!")
            else:
                await reply.reply("❌ Wrong!")

        elif game_name == "truth":
            truths = ["What is your biggest fear?", "What is your secret talent?"]
            await event.reply(f"🗣 Truth: {random.choice(truths)}")

        elif game_name == "dare":
            dares = ["Send a funny selfie!", "Type your last 3 emojis."]
            await event.reply(f"🔥 Dare: {random.choice(dares)}")

        elif game_name == "country":
            await event.reply(f"🌍 Guess this country: {random.choice(COUNTRIES)}")

        elif game_name == "flag":
            flags = {"🇮🇳": "India", "🇺🇸": "USA", "🇯🇵": "Japan"}
            flag, name = random.choice(list(flags.items()))
            await event.reply(f"Guess the country: {flag}")

        elif game_name == "scramble":
            word = random.choice(WORDS)
            scrambled = "".join(random.sample(word, len(word)))
            await event.reply(f"🔤 Unscramble this: `{scrambled}`")

        elif game_name == "quiz":
            await event.reply(f"🎓 Who won the 2018 FIFA World Cup? (France)")

        elif game_name == "animal":
            await event.reply(f"🐾 Guess this animal: {random.choice(ANIMALS)}")

        elif game_name == "memory":
            seq = [random.randint(1, 9) for _ in range(5)]
            await event.reply(f"🧠 Memorize this sequence: {' '.join(map(str, seq))}")
            await asyncio.sleep(3)
            await event.reply("What was the sequence?")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.strip() == " ".join(map(str, seq)):
                await reply.reply("🎉 Correct!")
            else:
                await reply.reply(f"❌ Wrong! It was {' '.join(map(str, seq))}.")

        elif game_name == "mathrace":
            a, b = random.randint(1, 20), random.randint(1, 20)
            await event.reply(f"⚡ Solve quickly: {a} x {b} = ?")
            reply = await client.wait_for(events.NewMessage(from_users=event.sender_id))
            if reply.raw_text.strip() == str(a * b):
                await reply.reply("🎉 You win!")
            else:
                await reply.reply(f"❌ Wrong! Answer is {a*b}.")
