from telethon import events
from config import OWNER_ID, DEEPL_API_KEY
import requests

try:
    from googletrans import Translator
    translator = Translator()
except ImportError:
    translator = None


# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def deepl_translate(text, target_lang="EN"):
    """Translate text using DeepL API if available."""
    if not DEEPL_API_KEY:
        return None
    url = "https://api-free.deepl.com/v2/translate"
    data = {"auth_key": DEEPL_API_KEY, "text": text, "target_lang": target_lang.upper()}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("translations", [{}])[0].get("text")
    return None


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.tr ?(\w{2})? (.+)"))
    @is_owner
    async def translate_cmd(event):
        """Translates text to target language."""
        target_lang = event.pattern_match.group(1)
        text = event.pattern_match.group(2)

        if not target_lang:
            target_lang = "en"  # Default to English

        await event.edit(f"🌐 **Translating to {target_lang.upper()}...**")

        try:
            translated_text = deepl_translate(text, target_lang)
            if not translated_text and translator:
                translated_text = translator.translate(text, dest=target_lang).text

            if not translated_text:
                return await event.edit("❌ Translation failed. Check API or library.")

            await event.edit(f"**Translated ({target_lang.upper()}):**\n`{translated_text}`")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
