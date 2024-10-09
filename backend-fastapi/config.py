import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

try:
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(str(BASE_DIR / ".env")))
except ImportError:
    print("not able to import .env")
    exit()

DATABASE_URI = os.environ.get("DATABASE_URI", "")
