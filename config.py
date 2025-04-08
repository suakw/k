from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
SESSION_STRING = getenv("SESSION_STRING")
DEV_CHANNEL = getenv("DEV_CHANNEL")
DEV_USER = getenv("DEV_USER")
OWNER_ID = int(getenv("OWNER_ID", "8033256866"))
COOK_PATH = getenv("COOK_PATH")
MAX_DURATION_MINUTES = int(getenv("MAX_DURATION_MINUTES", 30))
sudo_users_str = getenv("SUDO_USERS", "8033256866")
SUDO_USERS = [int(x) for x in sudo_users_str.split(',') if x.strip().isdigit()] if sudo_users_str else []
LOG_FILE_NAME = "YMusic.txt"
