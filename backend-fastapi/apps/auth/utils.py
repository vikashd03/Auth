import datetime
from typing import Optional
from fastapi import HTTPException, status
from fastapi.datastructures import Headers
import jwt
from passlib.context import CryptContext

from .models import UserModel, Users
from config import (
    ACCESS_TOKEN_EXPIRY_TIME,
    ACCESS_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_EXPIRY_TIME,
    JWT_ALGORITHM,
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "argon2", "bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class TOKEN_TYPE:
    REFRESH = "refresh"
    ACCESS = "access"


def create_token(data: dict, token_type: TOKEN_TYPE):
    payload = data.copy()
    secret = (
        ACCESS_TOKEN_SECRET_KEY
        if token_type == TOKEN_TYPE.ACCESS
        else REFRESH_TOKEN_SECRET_KEY
    )
    expiry_time = int(
        datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    ) + int(
        ACCESS_TOKEN_EXPIRY_TIME
        if token_type == TOKEN_TYPE.ACCESS
        else REFRESH_TOKEN_EXPIRY_TIME
    )
    payload.update({"expiryAt": expiry_time})
    encoded_jwt = jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    if not hashed_password or not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(
            msg="Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED
        )


def decode_token(token: str, token_type: TOKEN_TYPE) -> Optional[dict]:
    secret = (
        ACCESS_TOKEN_SECRET_KEY
        if token_type == TOKEN_TYPE.ACCESS
        else REFRESH_TOKEN_SECRET_KEY
    )
    try:
        decoded = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        return decoded
    except Exception as exce:
        print("decode JWT -", exce)
        return None


def user_authenticated(
    headers: Headers,
    token_type: TOKEN_TYPE,
    token: str = '',
) -> Optional[UserModel]:
    if token_type == TOKEN_TYPE.ACCESS and (
        "authorization" not in headers.keys()
        or headers["authorization"].split(" ")[0] != "Bearer"
        or not headers["authorization"].split(" ")[1]
    ):
        raise HTTPException(
            detail="User not Authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    token: str = (
        headers["authorization"].split(" ")[1]
        if token_type == TOKEN_TYPE.ACCESS
        else token
    )
    decoded_token = decode_token(token, token_type)
    if not decoded_token:
        raise HTTPException(
            detail="User not Authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user_id, expiryAt = decoded_token["user_id"], decoded_token["expiryAt"]
    current_utc_time = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    user = Users.get_user_by_id(user_id)
    if not user or expiryAt < current_utc_time:
        raise HTTPException(
            detail="User not Authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return user
