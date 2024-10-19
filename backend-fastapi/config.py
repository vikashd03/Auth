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

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_SECRET_KEY = os.environ.get(
    "ACCESS_TOKEN_SECRET_KEY", "jw1NdpVH5uz6bqKIHaZ"
)
REFRESH_TOKEN_SECRET_KEY = os.environ.get(
    "REFRESH_TOKEN_SECRET_KEY", "NRyLcO6exLpHMmTRAt5"
)

ACCESS_TOKEN_EXPIRY_TIME = os.environ.get("ACCESS_TOKEN_EXPIRY_TIME", 3600)
REFRESH_TOKEN_EXPIRY_TIME = os.environ.get("REFRESH_TOKEN_EXPIRY_TIME", 10000)

GENERAL_API_ERROR_RESPONSE = "Something went wrong"

BASE_ROUTE = "/api"