import os
from dotenv import load_dotenv

load_dotenv()


# '914674179'
ALLOWED_USERS = []
ADMINS = [914674179, ]
PGDB = str(os.getenv("PGDB"))
PGUSER =str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
ADMIN_KEY = str(os.getenv("ADMIN_KEY"))
IP = 'localhost'
KEY = str(os.getenv("KEY"))
