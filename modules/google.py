import requests
from telethon import events
from config import OWNER_ID, GOOGLE_API_KEY, GOOGLE_CSE_ID

SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

def google_search(query):
    try:
        params = {
            "q": query,
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CSE_ID,
            "num": 5,
        }
        response = requests.get(SEARCH_URL, params=params)
        data = response.json()
        results = data.get("items", [])
        return [
            f"🔍 [{item['title']}]({item['link']})\n{item['snippet']}"
            for item in results
        ]
    except Exception as e:
        return [f"❌ Error: {str(e)}"]

def register(client):
    @client.on(events.NewMessage(pattern=r"\.google (.+)"))
    async def google_handler(event):
        if event.sender_id != OWNER_ID:
            return
        query = event.pattern_match.group(1)
        await event.respond("🔎 **Searching Google...**")
        results = google_search(query)
        message = "\n\n".join(results) if results else "❌ No results found."
        await event.edit(f"**Google Search for:** `{query}`\n\n{message}", link_preview=False)

    @client.on(events.NewMessage(pattern=r"\.lmgtfy (.+)"))
    async def lmgtfy_handler(event):
        if event.sender_id != OWNER_ID:
            return
        query = event.pattern_match.group(1)
        link = f"https://lmgtfy.app/?q={query.replace(' ', '+')}"
        await event.respond(f"🤖 **Let me Google that for you:** [Click Here]({link})")
