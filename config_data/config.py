from environs import Env
import os

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
ADMIN_IDS = env("ADMIN_IDS")

BOT_PROXY = os.environ.get("BOT_PROXY", None)
TIME_ZONE = os.environ.get("TIME_ZONE", 5)  # utc +

