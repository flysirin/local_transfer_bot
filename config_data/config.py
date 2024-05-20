from os import environ


BOT_TOKEN = environ.get("BOT_TOKEN", None)
ADMIN_IDS = environ.get("ADMIN_IDS", None)

BOT_PROXY = environ.get("BOT_PROXY", None)
TIME_ZONE = environ.get("TIME_ZONE", 5)  # utc +

