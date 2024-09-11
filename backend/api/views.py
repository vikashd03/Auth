from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpRequest

from .handlers import CustomHTTPException, handle_error, is_http_res
from .utils import (
    check_required_fields,
    create_token,
    get_password_hash,
    user_authenticated,
    validate_email_format,
    verify_password,
)
from .db import UserTable
from .config import REFRESH_TOKEN_EXPIRY_TIME

# Create your views here.


@api_view(["POST"])
@handle_error(is_view=True)
def signup(request: HttpRequest):
    data = request.data
    _res = check_required_fields(data, ["name", "email", "password"])
    if is_http_res(_res):
        return _res
    if UserTable.get_user_by_email(data["email"].lower()):
        raise CustomHTTPException(
            msg="Email already taken", status=status.HTTP_400_BAD_REQUEST
        )
    hashed = get_password_hash(data["password"])
    user = UserTable.insert_user(
        data["email"],
        data["name"],
        hashed,
    )
    if not user:
        raise Exception("not able to create user")
    access_token = create_token({"user_id": user["id"]}, "access")
    refresh_token = create_token(
        {"user_id": user["id"], "email": user["email"]}, "refresh"
    )
    response = Response(
        data={
            "access_token": access_token,
            "email": user["email"],
            "name": user["name"],
        },
        status=status.HTTP_201_CREATED,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=timedelta(seconds=int(REFRESH_TOKEN_EXPIRY_TIME)),
        httponly=True,
        secure=True,
        samesite="None",
    )
    return response


@api_view(["POST"])
@handle_error(is_view=True)
def signin(request: HttpRequest):
    data = request.data
    _res = check_required_fields(data, ["email", "password"])
    if is_http_res(_res):
        return _res
    user = UserTable.get_user_by_email(data["email"].lower())
    if not user:
        raise CustomHTTPException(
            msg="User not found", status=status.HTTP_400_BAD_REQUEST
        )
    _res = verify_password(data["password"], user["password"])
    if is_http_res(_res):
        return _res
    access_token = create_token({"user_id": user["id"]}, "access")
    refresh_token = create_token(
        {"user_id": user["id"], "email": user["email"]}, "refresh"
    )
    response = Response(
        data={
            "access_token": access_token,
            "email": user["email"],
            "name": user["name"],
        },
        status=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=timedelta(seconds=int(REFRESH_TOKEN_EXPIRY_TIME)),
        httponly=True,
        secure=True,
        samesite="None",
    )
    return response


@api_view(["GET"])
@handle_error(is_view=True)
def refresh_token(request: HttpRequest):
    _res = check_required_fields(dict(request.COOKIES), ["refresh_token"], True)
    if is_http_res(_res):
        return _res
    refresh_token = request.COOKIES.get("refresh_token")
    user_res = user_authenticated(token_type="refresh", token=refresh_token)
    if is_http_res(user_res):
        return user_res
    access_token = create_token({"user_id": user_res["id"]}, "access")
    return Response(data={"access_token": access_token}, status=status.HTTP_200_OK)


@api_view(["POST"])
@handle_error(is_view=True)
def logout(request: HttpRequest):
    response = Response(
        data={"msg": "logged out successfully"},
        status=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="refresh_token",
        value=None,
        httponly=True,
        secure=True,
        samesite="None",
    )
    response.delete_cookie("refresh_token")
    return response


@api_view(["GET"])
@handle_error(is_view=True)
def get_users(request: HttpRequest):
    users = UserTable.get_all_users()
    users = users if users else []
    return Response(
        data={"data": users, "total": len(users)}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@handle_error(is_view=True)
def get_user(request: HttpRequest):
    user = request.session["user"]
    return Response(data=user, status=status.HTTP_200_OK)


@api_view(["POST"])
@handle_error(is_view=True)
def update_email(request: HttpRequest):
    data = request.data
    _res = check_required_fields(data, ["email"])
    if is_http_res(_res):
        return _res
    _res = validate_email_format(data["email"])
    if is_http_res(_res):
        return _res
    user = request.session["user"]
    updated_user = UserTable.update_email_by_id(user["id"], data["email"])
    if updated_user:
        return Response(
            data={
                "email": updated_user["email"],
                "message": "Email Updated",
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        raise Exception("error in updating email")


@api_view(["POST"])
@handle_error(is_view=True)
def update_username(request: HttpRequest):
    data = request.data
    _res = check_required_fields(data, ["name"])
    if is_http_res(_res):
        return _res
    user = request.session["user"]
    updated_user = UserTable.update_username_by_id(user["id"], data["name"])
    if updated_user:
        return Response(
            data={
                "name": updated_user["name"],
                "message": "User Name Updated",
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        raise Exception("error in updating user name")


@api_view(["POST"])
@handle_error(is_view=True)
def update_password(request: HttpRequest):
    data = request.data
    _res = check_required_fields(data, ["password"])
    if is_http_res(_res):
        return _res
    hashed = get_password_hash(data["password"])
    user = request.session["user"]
    updated_user = UserTable.update_password_by_id(user["id"], hashed)
    if updated_user:
        return Response(
            data={
                "name": updated_user["name"],
                "email": updated_user["email"],
                "message": "Password Updated",
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        raise Exception("not able to update password")

