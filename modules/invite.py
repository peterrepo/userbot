import asyncio
import json
import os
from telethon import events
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.errors import (
    UserAlreadyParticipantError,
    UserPrivacyRestrictedError,
    FloodWaitError,
)
from telethon.tl.types import PeerUser
from config import OWNER_ID

# ==============================
# File for scraped members
# ==============================
os.makedirs("data", exist_ok=True)
SCRAPED_FILE = "data/scraped_members.json"
if not os.path.exists(SCRAPED_FILE):
    with open(SCRAPED_FILE, "w") as f:
        json.dump([], f, indent=2)


def register(client):
    async def safe_respond(event, message, delay=5):
        msg = await event.respond(message)
        await asyncio.sleep(delay)
        await msg.delete()

    async def resolve_entity(client, identifier):
        if identifier.isdigit():
            try:
                return await client.get_entity(PeerUser(int(identifier)))
            except Exception:
                return None
        else:
            try:
                return await client.get_entity(identifier)
            except Exception:
                return None

    async def invite_user_to_chat(client, chat_id, user):
        """
        Invite user to chat or channel based on chat type.
        """
        try:
            entity = await client.get_entity(chat_id)
            if hasattr(entity, "megagroup") or hasattr(entity, "broadcast"):  # Channel or Supergroup
                await client(InviteToChannelRequest(entity, [user]))
            else:  # Normal group
                await client(AddChatUserRequest(entity.id, user, fwd_limit=0))
        except UserAlreadyParticipantError:
            raise UserAlreadyParticipantError
        except Exception as e:
            raise e

    # ==============================
    # SCRAPE MEMBERS
    # ==============================
    @client.on(events.NewMessage(pattern=r"^\.scrapemembers (.+)"))
    async def scrape_members(event):
        if event.sender_id != OWNER_ID:
            return

        source = event.pattern_match.group(1).strip()
        await event.respond(f"🔍 Scraping members from: {source} ...")

        try:
            members = []
            async for user in client.iter_participants(source):
                members.append({"id": user.id, "name": user.first_name or "NoName"})

            with open(SCRAPED_FILE, "w") as f:
                json.dump(members, f, indent=2)

            await event.respond(
                f"✅ Scraped {len(members)} members from {source}.\nSaved to {SCRAPED_FILE}."
            )
        except Exception as e:
            await event.respond(f"❌ Error scraping members: {e}")

    # ==============================
    # MASS INVITE FROM SCRAPED FILE
    # ==============================
    @client.on(events.NewMessage(pattern=r"^\.massinvite$"))
    async def mass_invite(event):
        if event.sender_id != OWNER_ID:
            return

        if not os.path.exists(SCRAPED_FILE):
            await event.respond("❌ **No scraped members found. Use .scrapemembers <group> first.**")
            return

        with open(SCRAPED_FILE, "r") as f:
            members = json.load(f)

        msg = await event.respond(f"🚀 **Starting mass invite for {len(members)} users...**")

        success, failed = 0, 0
        for user_data in members:
            try:
                user_id = user_data["id"]
                user = await resolve_entity(client, str(user_id))
                if user:
                    await invite_user_to_chat(client, event.chat_id, user)
                    success += 1
                    await asyncio.sleep(2)
                else:
                    failed += 1
            except UserAlreadyParticipantError:
                failed += 1
            except UserPrivacyRestrictedError:
                failed += 1
            except FloodWaitError as f:
                await msg.edit(f"⚠️ **Flood wait: sleeping for {f.seconds} seconds.**")
                await asyncio.sleep(f.seconds)
            except Exception:
                failed += 1

        await msg.edit(f"✅ Mass invite completed.**\n**Success: {success}\n**Failed:** {failed}")

    # ==============================
    # MASS SCRAPE + INVITE
    # ==============================
    @client.on(events.NewMessage(pattern=r"^\.massinvitefrom (.+)"))
    async def mass_invite_from(event):
        if event.sender_id != OWNER_ID:
            return

        source = event.pattern_match.group(1).strip()
        await event.respond(f"🔍 Scraping and inviting members from: {source} ...")

        try:
            members = []
            async for user in client.iter_participants(source):
                members.append({"id": user.id, "name": user.first_name or "NoName"})

            await event.respond(f"✅ **Scraped {len(members)} members from {source}. Starting invites...**")

            success, failed = 0, 0
            for user_data in members:
                try:
                    user = await resolve_entity(client, str(user_data["id"]))
                    if user:
                        await invite_user_to_chat(client, event.chat_id, user)
                        success += 1
                        await asyncio.sleep(2)
                    else:
                        failed += 1
                except UserAlreadyParticipantError:
                    failed += 1
                except UserPrivacyRestrictedError:
                    failed += 1
                except FloodWaitError as f:
                    await event.respond(f"⚠️ **Flood wait: sleeping for {f.seconds} seconds.**")
                    await asyncio.sleep(f.seconds)
                except Exception:
                    failed += 1

            await event.respond(f"✅ Mass invite completed.**\n**Success: {success}\n**Failed:** {failed}")

        except Exception as e:
            await event.respond(f"❌ Error during mass scrape/invite: {e}")

    # ==============================
    # DIRECT INVITE
    # ==============================
    @client.on(events.NewMessage(pattern=r"^\.invite ?(.*)"))
    async def invite_user(event):
        if event.sender_id != OWNER_ID:
            return

        args = event.pattern_match.group(1).strip()
        if not args and not event.is_reply:
            await safe_respond(event, "⚠️ Usage: `.invite <username or user_id>`")
            return

        try:
            if event.is_reply:
                reply = await event.get_reply_message()
                user = await client.get_entity(reply.sender_id)
            else:
                user = await resolve_entity(client, args)

            if not user:
                await safe_respond(event, f"❌ User not found: `{args}`")
                return

            await invite_user_to_chat(client, event.chat_id, user)
            await event.respond(f"✅ Invited: `{getattr(user, 'username', user.id)}`")
        except UserAlreadyParticipantError:
            await safe_respond(event, "⚠️ **User is already in this group.**")
        except UserPrivacyRestrictedError:
            await safe_respond(event, "⚠️ **User's privacy settings prevent invites.**")
        except Exception as e:
            await safe_respond(event, f"❌ Error inviting user: {e}")
