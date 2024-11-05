import datetime
import os
from pathlib import Path
from typing import Optional
from fastapi import HTTPException, WebSocketException, status
import jwt
from passlib.context import CryptContext
from enum import Enum

from apps.chat.utils import ChatType

from .schemas import AccessTokenPayload, RefreshTokenPayload, UserModel
from .crud import Users
from config import (
    ACCESS_TOKEN_EXPIRY_TIME,
    ACCESS_TOKEN_SECRET_KEY,
    BASE_DIR,
    PROFILE_IMAGE_DIR_PATH,
    REFRESH_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_EXPIRY_TIME,
    JWT_ALGORITHM,
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "argon2", "bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class TOKEN_TYPE(str, Enum):
    REFRESH = "refresh"
    ACCESS = "access"


class REQUEST_TYPE(str, Enum):
    HTTP = "http"
    WEBSOCKET = "websocket"


PROFILE_IMAGE_TYPES = ["user", "group"]


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
            detail="Invalid Credentials", status_code=status.HTTP_401_UNAUTHORIZED
        )


def decode_token(
    token: str, token_type: TOKEN_TYPE
) -> Optional[AccessTokenPayload | RefreshTokenPayload]:
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


def raise_not_authenticated(request_type: REQUEST_TYPE):
    if request_type == REQUEST_TYPE.HTTP:
        raise HTTPException(
            detail="User not Authenticated",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    elif request_type == REQUEST_TYPE.WEBSOCKET:
        raise WebSocketException(
            reason="User not Authenticated",
            code=status.WS_1008_POLICY_VIOLATION,
        )


def user_authenticated(
    data: dict[str, str],
    token_type: TOKEN_TYPE,
    request_type: REQUEST_TYPE = REQUEST_TYPE.HTTP,
    token: str = "",
) -> Optional[UserModel]:
    if token_type == TOKEN_TYPE.ACCESS and (
        "authorization" not in data.keys()
        or not data["authorization"].startswith("Bearer ")
        or not data["authorization"].removeprefix("Bearer ")
    ):
        raise_not_authenticated(request_type)
    token = (
        data["authorization"].removeprefix("Bearer ")
        if token_type == TOKEN_TYPE.ACCESS
        else token
    )
    decoded_token = decode_token(token, token_type)
    if not decoded_token:
        raise_not_authenticated(request_type)
    user_id, expiryAt = decoded_token["user_id"], decoded_token["expiryAt"]
    current_utc_time = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    user = Users.get_user_by_id(user_id)
    if not user or expiryAt < current_utc_time:
        raise_not_authenticated(request_type)
    return user


def get_profile_image_url(id: int, type: ChatType) -> str | None:
    file_name_search = f"{id}.*"
    found_files = list(
        Path(
            f"{PROFILE_IMAGE_DIR_PATH}/{'user' if type == ChatType.DIRECT else 'group'}"
        ).glob(file_name_search)
    )
    if len(found_files) > 0:
        file_path = found_files[0]
        if os.path.isfile(file_path):
            return str(file_path).replace(f"{BASE_DIR}/", "")
    return None
