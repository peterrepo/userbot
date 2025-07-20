from telethon import events
from config import OWNER_ID
import wikipedia

# Set Wikipedia language to English
wikipedia.set_lang("en")

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.wiki (.+)"))
    @is_owner
    async def wiki_search(event):
        """Fetch a summary from Wikipedia."""
        query = event.pattern_match.group(1).strip()
        await event.edit(f"🔍 **Searching Wikipedia for:** `{query}`")

        try:
            summary = wikipedia.summary(query, sentences=3)
            await event.edit(f"**Wikipedia:** {query}\n\n{summary}")
        except wikipedia.DisambiguationError as e:
            options = "\n".join(e.options[:5])
            await event.edit(f"⚠ **Multiple results found:**\n{options}")
        except wikipedia.PageError:
            await event.edit("❌ No page found for this query.")
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
