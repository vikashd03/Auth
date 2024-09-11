import os

ALGORITHM = "HS256"

ACCESS_TOKEN_SECRET_KEY = os.environ.get(
    "ACCESS_TOKEN_SECRET_KEY", "jw1NdpVH5uz6bqKIHaZ"
)
REFRESH__TOKEN_SECRET_KEY = os.environ.get(
    "REFRESH__TOKEN_SECRET_KEY", "NRyLcO6exLpHMmTRAt5"
)
ACCESS_TOKEN_EXPIRY_TIME = os.environ.get("ACCESS_TOKEN_EXPIRY_TIME", 3600)
REFRESH_TOKEN_EXPIRY_TIME = os.environ.get("REFRESH_TOKEN_EXPIRY_TIME", 10000)

UNPROTECTED_ROUTES = ["signup/", "signin/", "refresh/token/", "logout/"]

BASE_ROUTE = "api/"

GENERAL_API_ERROR_RESPONSE = "Something went wrong"
