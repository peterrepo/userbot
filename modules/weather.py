import requests
from telethon import events
from config import OWNER_ID, WEATHER_API_KEY

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"

# Owner check decorator
def is_owner(func):
    async def wrapper(event, *args, **kwargs):
        if event.sender_id != OWNER_ID:
            await event.reply("❌ You are not authorized to use this command.")
            return
        return await func(event, *args, **kwargs)
    return wrapper


def get_weather(city):
    """Fetch weather data from OpenWeatherMap."""
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        main = data["main"]
        weather = data["weather"][0]["description"]
        wind = data["wind"]["speed"]
        temp = main["temp"]
        feels_like = main["feels_like"]
        humidity = main["humidity"]
        return f"**Weather in {city.title()}**\n" \
               f"🌡 Temp: {temp}°C (Feels like {feels_like}°C)\n" \
               f"💧 Humidity: {humidity}%\n" \
               f"🌬 Wind: {wind} m/s\n" \
               f"☁ Condition: {weather.title()}"
    else:
        return None


def register(client):

    @client.on(events.NewMessage(pattern=r"^\.weather (.+)"))
    @is_owner
    async def weather_cmd(event):
        """Fetch weather for a given city."""
        city = event.pattern_match.group(1).strip()
        if not WEATHER_API_KEY:
            return await event.edit("❌ OpenWeatherMap API Key not configured in `config.py`.")

        await event.edit(f"☁ **Fetching weather for {city}...**")

        try:
            result = get_weather(city)
            if not result:
                return await event.edit("❌ Could not fetch weather data. Check city name.")
            await event.edit(result)
        except Exception as e:
            await event.edit(f"❌ Error: {e}")
