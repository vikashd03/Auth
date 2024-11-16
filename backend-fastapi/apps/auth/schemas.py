from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    password: str
    active: bool
    img_url: Optional[str] = None


class SiginUpFormData(BaseModel):
    name: str
    email: str
    password: str


class SiginInFormData(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    name: str
    email: str
    active: bool
    access_token: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    active: bool
    img_url: Optional[str] = None


class UsersResponse(BaseModel):
    data: List[UserResponse]
    total: int


class RefreshTokenResponse(BaseModel):
    access_token: str


class AccessTokenPayload(BaseModel):
    user_id: str
    expiryAt: int


class RefreshTokenPayload(BaseModel):
    user_id: str
    email: str
    expiryAt: int


class UpdateUserNameFormData(BaseModel):
    name: str
