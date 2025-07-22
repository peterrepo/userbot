import requests
from telethon import events
from config import OWNER_ID

API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"


def register(client):
    @client.on(events.NewMessage(pattern=r"^\.dict (.+)"))
    async def dictionary_handler(event):
        if event.sender_id != OWNER_ID:
            return  # Owner-only command

        word = event.pattern_match.group(1).strip()
        await event.edit(f"🔍 **Searching meaning for:** `{word}`...")

        try:
            response = requests.get(API_URL.format(word))
            if response.status_code != 200:
                await event.edit(f"❌ No results found for `{word}`.")
                return

            data = response.json()[0]
            word_title = data.get("word", word).capitalize()

            # Meanings
            meanings = data.get("meanings", [])
            message = f"**📖 {word_title}**\n\n"

            for meaning in meanings:
                part_of_speech = meaning.get("partOfSpeech", "N/A").capitalize()
                definitions = meaning.get("definitions", [])

                message += f"**({part_of_speech})**\n"
                for idx, definition in enumerate(definitions[:2], start=1):
                    definition_text = definition.get("definition", "No definition available.")
                    example = definition.get("example", None)
                    message += f"  {idx}. {definition_text}\n"
                    if example:
                        message += f"     _Example_: {example}\n"

                # Synonyms
                synonyms = meaning.get("synonyms", [])
                if synonyms:
                    message += f"  **Synonyms:** {', '.join(synonyms[:5])}\n"

                # Antonyms
                antonyms = meaning.get("antonyms", [])
                if antonyms:
                    message += f"  **Antonyms:** {', '.join(antonyms[:5])}\n"

                message += "\n"

            await event.edit(message[:4096])  # Limit message to Telegram max chars

        except Exception as e:
            await event.edit(f"⚠️ **Error:** {str(e)}")
