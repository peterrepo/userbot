import aiohttp
from telethon import events
from config import OWNER_ID

GITHUB_API_URL = "https://api.github.com"

def register(client):
    @client.on(events.NewMessage(pattern=r"\.gitrepo (.+)"))
    async def git_repo_info(event):
        if event.sender_id != OWNER_ID:
            return
        
        repo_name = event.pattern_match.group(1).strip()
        if not repo_name:
            await event.respond("❌ **Usage:** `.gitrepo <username/repo>`")
            return

        await event.respond(f"🔎 **Fetching repository info for:** `{repo_name}` ...")
        await event.delete()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{GITHUB_API_URL}/repos/{repo_name}") as response:
                    if response.status != 200:
                        await event.respond(f"❌ **Repository not found:** `{repo_name}`")
                        return
                    data = await response.json()

            repo_info = (
                f"**📦 Repository:** [{data['full_name']}]({data['html_url']})\n"
                f"**⭐ Stars:** {data['stargazers_count']}\n"
                f"**🍴 Forks:** {data['forks_count']}\n"
                f"**🐛 Issues:** {data['open_issues_count']}\n"
                f"**📜 Description:** `{data['description']}`\n"
                f"**🕒 Updated:** `{data['updated_at']}`"
            )
            await event.respond(repo_info, link_preview=False)

        except Exception as e:
            await event.respond(f"⚠ **Error fetching repo info:** {str(e)}")

    @client.on(events.NewMessage(pattern=r"\.gituser (.+)"))
    async def git_user_info(event):
        if event.sender_id != OWNER_ID:
            return

        username = event.pattern_match.group(1).strip()
        if not username:
            await event.respond("❌ **Usage:** `.gituser <username>`")
            return

        await event.respond(f"🔎 **Fetching user info for:** `{username}` ...")
        await event.delete()

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{GITHUB_API_URL}/users/{username}") as response:
                    if response.status != 200:
                        await event.respond(f"❌ **User not found:** `{username}`")
                        return
                    data = await response.json()

            user_info = (
                f"**👤 User:** [{data['login']}]({data['html_url']})\n"
                f"**🏢 Company:** `{data.get('company', 'N/A')}`\n"
                f"**📍 Location:** `{data.get('location', 'N/A')}`\n"
                f"**📜 Bio:** `{data.get('bio', 'N/A')}`\n"
                f"**🔗 Public Repos:** `{data['public_repos']}`\n"
                f"**👥 Followers:** `{data['followers']}` | **Following:** `{data['following']}`"
            )
            await event.respond(user_info, link_preview=False)

        except Exception as e:
            await event.respond(f"⚠ **Error fetching user info:** {str(e)}")
