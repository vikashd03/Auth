import datetime
import re
from typing import List, Optional
from rest_framework import status
from passlib.context import CryptContext
import jwt

from .handlers import CustomHTTPException, handle_error

from .db import UserTable
from .config import (
    ACCESS_TOKEN_EXPIRY_TIME,
    ACCESS_TOKEN_SECRET_KEY,
    JWT_ALGORITHM,
    GENERAL_API_ERROR_RESPONSE,
    REFRESH_TOKEN_SECRET_KEY,
    REFRESH_TOKEN_EXPIRY_TIME,
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "argon2", "bcrypt"])


@handle_error()
def verify_password(plain_password, hashed_password):
    if not hashed_password or not pwd_context.verify(plain_password, hashed_password):
        raise CustomHTTPException(
            msg="Invalid Credentials", status=status.HTTP_401_UNAUTHORIZED
        )


@handle_error()
def get_password_hash(password):
    return pwd_context.hash(password)


@handle_error()
def create_token(data: dict, token_type: str = "access"):
    payload = data.copy()
    secret = (
        ACCESS_TOKEN_SECRET_KEY if token_type == "access" else REFRESH_TOKEN_SECRET_KEY
    )
    expiry_time = int(
        datetime.datetime.now(tz=datetime.timezone.utc).timestamp()
    ) + int(
        ACCESS_TOKEN_EXPIRY_TIME
        if token_type == "access"
        else REFRESH_TOKEN_EXPIRY_TIME
    )
    payload.update({"expiryAt": expiry_time})
    encoded_jwt = jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)
    return encoded_jwt


@handle_error()
def decode_token(token: str, token_type: str = "access") -> Optional[dict]:
    secret = (
        ACCESS_TOKEN_SECRET_KEY if token_type == "access" else REFRESH_TOKEN_SECRET_KEY
    )
    decoded = jwt.decode(
        token,
        secret,
        algorithms=[JWT_ALGORITHM],
    )
    return decoded


@handle_error()
def check_required_fields(data: dict, fields: List[str], is_auth: str = False):
    fields_not_found = []
    for field in fields:
        if field not in data.keys():
            fields_not_found.append(field)
    if len(fields_not_found) > 0:
        raise CustomHTTPException(
            msg=f"{', '.join(fields_not_found)} {'field' if len(fields_not_found) == 1 else 'fields'} not found in request {'body' if not is_auth else'cookies'}",
            status=(
                status.HTTP_400_BAD_REQUEST
                if not is_auth
                else status.HTTP_401_UNAUTHORIZED
            ),
        )


@handle_error()
def validate_email_format(email: str) -> bool:
    if not bool(re.match(r"[^@]+@[^@]+\.[^@]+", email)):
        raise CustomHTTPException(
            msg="email is invalid",
            status=status.HTTP_400_BAD_REQUEST,
        )


@handle_error()
def user_authenticated(headers: dict = {}, token_type: str = "access", token: str = ""):
    if token_type == "access" and (
        "Authorization" not in headers.keys()
        or headers["Authorization"].split(" ")[0] != "Bearer"
        or not headers["Authorization"].split(" ")[1]
    ):
        raise CustomHTTPException(
            msg=GENERAL_API_ERROR_RESPONSE,
            status=status.HTTP_401_UNAUTHORIZED,
        )
    token: str = (
        headers["Authorization"].split(" ")[1] if token_type == "access" else token
    )
    decoded_token = decode_token(token, token_type)
    user_id, expiryAt = decoded_token["user_id"], decoded_token["expiryAt"]
    current_utc_time = int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    user = UserTable.get_user_by_id(user_id)
    if not user or expiryAt < current_utc_time:
        raise CustomHTTPException(
            msg="Unauthorized",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return user
