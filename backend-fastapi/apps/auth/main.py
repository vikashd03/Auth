from datetime import timedelta
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File, HTTPException, Request, Response, UploadFile, status
from fastapi.responses import FileResponse

from config import (
    BASE_DIR,
    PROFILE_IMAGE_FILE_TYPES,
    PROFILE_IMAGE_UPLOAD_DIR,
    REFRESH_TOKEN_EXPIRY_TIME,
)

from .utils import (
    TOKEN_TYPE,
    create_token,
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
    UserResponse,
    UsersResponse,
)
from .crud import Users

app = FastAPI()

register_exception_handlers(app)

profile_images_dir = f"{BASE_DIR}/{PROFILE_IMAGE_UPLOAD_DIR}/"
os.makedirs(profile_images_dir, exist_ok=True)


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
    return {"data": users, "total": len(users)}


@app.post("/profile-image")
def upload_profile_image(
    request: AppRequest, response: Response, file: UploadFile = File(...)
):
    if file.content_type not in PROFILE_IMAGE_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Only JPEG and PNG files are allowed.",
        )
    file_extension = file.filename.split(".")[-1]
    if not file_extension:
        file_extension = file.content_type.removeprefix("image/")
    file_name_search = f"{request.state.user.id}.*"
    old_profile_files = list(Path(profile_images_dir).glob(file_name_search))
    if len(old_profile_files) > 0:
        for file_path in old_profile_files:
            if os.path.isfile(file_path):
                os.remove(file_path)
    file_location = f"{profile_images_dir}{request.state.user.id}.{file_extension}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    response.status_code = status.HTTP_200_OK
    return {"msg": "Uploaded Successfully"}


@app.get("/profile-image")
def get_profile_image(request: AppRequest, response: Response):
    file_name_search = f"{request.state.user.id}.*"
    found_files = list(Path(profile_images_dir).glob(file_name_search))
    if len(found_files) > 0:
        file_path = found_files[0]
        if os.path.exists(file_path):
            response.status_code = status.HTTP_200_OK
            return FileResponse(file_path)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Profile Image not found",
    )
