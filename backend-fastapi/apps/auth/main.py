from datetime import timedelta
import os
from pathlib import Path
import shutil
from typing import Literal
from fastapi import FastAPI, File, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import FileResponse

from config import (
    PROFILE_IMAGE_DIR_PATH,
    PROFILE_IMAGE_FILE_TYPES,
    REFRESH_TOKEN_EXPIRY_TIME,
)

from .utils import (
    TOKEN_TYPE,
    PROFILE_IMAGE_TYPES,
    create_token,
    get_profile_image_url,
    hash_password,
    user_authenticated,
    verify_password,
)
from internal.utils import AppRequest, register_exception_handlers
from .schemas import (
    AuthResponse,
    RefreshTokenResponse,
    SiginInFormData,
    SiginUpFormData,
    UpdateUserNameFormData,
    UserResponse,
    UsersResponse,
)
from .crud import Users

app = FastAPI()

register_exception_handlers(app)

os.makedirs(PROFILE_IMAGE_DIR_PATH, exist_ok=True)


@app.post("/signup", response_model=AuthResponse)
def signup(response: Response, form_data: SiginUpFormData):
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


@app.post("/signin", response_model=AuthResponse)
def signin(response: Response, form_data: SiginInFormData):
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
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not Authenticated"
        )
    user = user_authenticated(
        data=None, token_type=TOKEN_TYPE.REFRESH, token=refresh_token
    )
    access_token = create_token({"user_id": user.id}, TOKEN_TYPE.ACCESS)
    response.status_code = status.HTTP_200_OK
    return {"access_token": access_token}


@app.post("/logout")
def logout(response: Response):
    response.status_code = status.HTTP_200_OK
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="None",
    )
    set_cookie_header = response.headers.get("set-cookie")
    if not set_cookie_header or 'refresh_token="";' not in set_cookie_header:
        print("cookie not deleted, setting it empty")
        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            secure=True,
            samesite="None",
            expires=0,
        )
    return {"msg": "logged out successfully"}


@app.get("/user", response_model=UserResponse)
def get_user(request: AppRequest, response: Response):
    user = request.state.user
    user.img_url = get_profile_image_url(user.id, "direct")
    if user:
        response.status_code = status.HTTP_200_OK
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )


@app.get("/users", response_model=UsersResponse)
def get_users(response: Response):
    response.status_code = status.HTTP_200_OK
    users = Users.get_all_users()
    for user in users:
        user.img_url = get_profile_image_url(user.id, "direct")
    return {"data": users, "total": len(users)}


@app.post("/profile-image/{type}/{id}")
def upload_profile_image(
    response: Response,
    type: Literal[*PROFILE_IMAGE_TYPES],  # type: ignore
    id: int,
    file: UploadFile = File(...),
):
    if file.content_type not in PROFILE_IMAGE_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only JPEG and PNG files are allowed.",
        )
    file_extension = file.filename.split(".")[-1]
    if not file_extension:
        file_extension = file.content_type.removeprefix("image/")
    file_name_search = f"{id}.*"
    files_dir_for_type = f"{PROFILE_IMAGE_DIR_PATH}/{str(type)}"
    old_profile_files = list(Path(files_dir_for_type).glob(file_name_search))
    if len(old_profile_files) > 0:
        for file_path in old_profile_files:
            if os.path.isfile(file_path):
                os.remove(file_path)
    file_location = f"{files_dir_for_type}/{id}.{file_extension}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    response.status_code = status.HTTP_200_OK
    return {"msg": "Uploaded Successfully"}


@app.put("/username")
def update_name(
    request: AppRequest, form_data: UpdateUserNameFormData, response: Response
):
    user = Users.update_name(request.state.user.id, form_data.name)
    response.status_code = status.HTTP_200_OK
    return {"data": user}
