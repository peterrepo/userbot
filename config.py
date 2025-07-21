import os 
BASE_DIR = "/home/godhunter/newgit/userbot"
DATA_DIR = os.path.join(BASE_DIR, "data")
GLOBALS_JSON = os.path.join(DATA_DIR, "globals.json")
# ======================
# TELEGRAM CONFIGURATION
# ======================
API_ID = 28289547  # Your Telegram API ID (from my.telegram.org)
API_HASH = "fb26885f55aad0acbda5ac7f3adf60f6"  # Your Telegram API Hash
SESSION_STRING = "1BVtsOIcBu0NeIURnwnRXBnvT2dOoo4hjNfZaiEXbaUYfivTI56JeCWotQ2TPpKTjm8gWygIYxOVZ17maNDraOw4PgLyqZGeltXAgswjuXrgioA5I7EMMcjNFVoJZeGUA5gNEmWUj_HBFTifZJqskklpwpqPhqAbuA0TSOeEBlkG-TpnGEs1U6wjkZJl5APoRzJNOVLFMTFPN87Se_9QH-x7QA5ppEFXWovvuWt7Gb_nqH_ntQK3sBJ1BrGq0jmyFNifHOMUT4cVyoE38gvKg0lsd46hgOjNxwHbI0MqXZZa4d6NHXrRsFYhy_05zC48udO1l7kvJVyApLHQxCY3d8F6wklBcrEM="  # Your Telethon session string
OWNER_ID = 7292202061  # Your Telegram user ID (owner)

# ======================
# DATABASE & STORAGE
# ======================
MONGO_DB_URI = ""     # MongoDB URI (for modules needing DB)
REDIS_URL = ""        # Redis server URL (optional)
SQL_DB_URL = ""       # SQLAlchemy Database URL

# ======================
# GOOGLE & AI SERVICES
# ======================
GOOGLE_API_KEY = "AIzaSyBWXm6c5bKyQaLwSDZ35nWmg38dTT8mH6U"  # Google API Key
GOOGLE_CSE_ID = "07ff5954378d54935"  # Google Custom Search Engine ID
YT_API_KEY = "AIzaSyBWXm6c5bKyQaLwSDZ35nWmg38dTT8mH6U"  # YouTube Data API Key
WEATHER_API_KEY = "10dd39ebd0e578efd3fcd22a0110e742"  # OpenWeatherMap API key
MAPS_API_KEY = ""  # Google Maps API Key

# ======================
# SOCIAL MEDIA MODULES
# ======================
INSTAGRAM_USERNAME = "serenehashira"  # Instagram username (for insta.py)
INSTAGRAM_PASSWORD = "tomioka2008"    # Instagram password
TWITTER_API_KEY = ""                  # Twitter API Key
TWITTER_API_SECRET = ""               # Twitter API Secret
TWITTER_BEARER_TOKEN = ""             # Twitter Bearer Token
TWITTER_ACCESS_TOKEN = ""             # Twitter Access Token
TWITTER_ACCESS_SECRET = ""            # Twitter Access Secret
TENOR_API_KEY = "AIzaSyBWXm6c5bKyQaLwSDZ35nWmg38dTT8mH6U"
MAX_SPAM_MESSAGES = 1000
SPAM_DELAY = 0.3
ENCRYPTION_KEY = ""
CSE_ID = "07ff5954378d54935" 
BITLY_API_KEY = "73ad55f43dbf8e5ed80b1e959eb80fa2a31701b7"
GDRIVE_API_KEY = "AIzaSyB-6IfMnLZpSq55Wc69Uqts3qmCY6ZmQgE"
GDRIVE_FOLDER_ID = "1dRGJynWK3Y33lww5VxQpdVIkck0RxXzb"
