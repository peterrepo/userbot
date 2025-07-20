import os
from gtts import gTTS
from telethon import events
from config import OWNER_ID

# Temporary file for audio
TEMP_AUDIO = "tts_output.mp3"

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.tts (.+)"))
    @is_owner
    async def text_to_speech(event):
        text = event.pattern_match.group(1).strip()
        await event.edit("🎙 **Generating speech...**")

        try:
            # Generate speech with gTTS
            tts = gTTS(text, lang="en")
            tts.save(TEMP_AUDIO)

            # Send the audio as a voice message
            await client.send_file(event.chat_id, TEMP_AUDIO, voice_note=True)
            await event.delete()

            os.remove(TEMP_AUDIO)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
