import os
from pathlib import Path

try:
    from dotenv import load_dotenv, find_dotenv

    PROJECT_BASE_DIR = Path(__file__).parent
    load_dotenv(find_dotenv(str(PROJECT_BASE_DIR / ".env")))
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

BASE_DIR = str(Path(__file__).resolve().parent)

UNPROTECTED_ROUTES = [
    "auth/signup/",
    "auth/signin/",
    "auth/refresh/token/",
    "auth/logout/",
]

ALLOWED_ORIGINS = ["http://localhost:5173"]

PROFILE_IMAGE_UPLOAD_DIR = os.environ.get(
    "PROFILE_IMAGE_UPLOAD_DIR", "data/profile-images"
)

PROFILE_IMAGE_DIR_PATH = f"{BASE_DIR}/{PROFILE_IMAGE_UPLOAD_DIR}"

PROFILE_IMAGE_FILE_TYPES = ["image/jpeg", "image/png"]
