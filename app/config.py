import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if BOT_TOKEN is None:
    raise RuntimeError("BOT_TOKEN is not set")

if ADMIN_ID is None:
    raise RuntimeError("ADMIN_ID is not set")

ADMIN_ID = int(ADMIN_ID)