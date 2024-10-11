from datetime import timedelta
from fastapi import FastAPI, HTTPException, Request, Response, status

from config import REFRESH_TOKEN_EXPIRY_TIME

from .utils import (
    TOKEN_TYPE,
    create_token,
    hash_password,
    user_authenticated,
    verify_password,
)
from internal.utils import register_exception_handlers
from .models import (
    RefreshTokenResponse,
    SiginInFormData,
    SiginUpFormData,
    UserResponse,
    Users,
)

app = FastAPI()

register_exception_handlers(app)


@app.post("/signup", response_model=UserResponse)
async def signup(response: Response, form_data: SiginUpFormData):
    if Users.get_user_by_email(form_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken"
        )
    user = Users.create_user(
        name=form_data.name,
        email=form_data.email,
        passowrd=hash_password(form_data.password),
    )
    if not user:
        raise HTTPException(detail="not able to create user")
    access_token = create_token({"user_id": user.id}, TOKEN_TYPE.ACCESS)
    refresh_token = create_token(
        {"user_id": user.id, "email": user.email}, TOKEN_TYPE.REFRESH
    )
    if user:
        response.status_code = status.HTTP_201_CREATED
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=timedelta(seconds=int(REFRESH_TOKEN_EXPIRY_TIME)),
            httponly=True,
            secure=True,
            samesite="None",
        )
        return {
            "access_token": access_token,
            "name": user.name,
            "email": user.email,
            "active": user.active,
        }


@app.post("/signin", response_model=UserResponse)
async def signin(response: Response, form_data: SiginInFormData):
    user = Users.get_user_by_email(form_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    verify_password(form_data.password, user.password)
    access_token = create_token({"user_id": user.id}, TOKEN_TYPE.ACCESS)
    refresh_token = create_token(
        {"user_id": user.id, "email": user.email}, TOKEN_TYPE.REFRESH
    )
    if user:
        response.status_code = status.HTTP_200_OK
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            max_age=timedelta(seconds=int(REFRESH_TOKEN_EXPIRY_TIME)),
            httponly=True,
            secure=True,
            samesite="None",
        )
        return {
            "access_token": access_token,
            "name": user.name,
            "email": user.email,
            "active": user.active,
        }


@app.get("/refresh/token", response_model=RefreshTokenResponse)
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not Authenticated"
        )
    user = user_authenticated(
        headers=None, token_type=TOKEN_TYPE.REFRESH, token=refresh_token
    )
    access_token = create_token({"user_id": user.id}, TOKEN_TYPE.ACCESS)
    response.status_code = status.HTTP_200_OK
    return {"access_token": access_token}
