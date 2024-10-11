from typing import Optional
from sqlalchemy import Boolean, Column, Integer, String

from internal.db import Base, get_db
from pydantic import BaseModel, ConfigDict


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50))
    email = Column(String(length=320), unique=True, index=True)
    password = Column(String(length=500))
    active = Column(Boolean, default=True)


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    password: str
    active: bool


class SiginUpFormData(BaseModel):
    name: str
    email: str
    password: str


class SiginInFormData(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    name: str
    email: str
    active: bool
    access_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str


class UserTable:
    def create_user(self, name: str, email: str, passowrd: str) -> Optional[UserModel]:
        with get_db() as db:
            user = User(**{"name": name, "email": email, "password": passowrd})
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        with get_db() as db:
            user = db.query(User).filter(User.email == email).first()
            if user:
                return UserModel.model_validate(user)
            else:
                return None

    def get_user_by_id(self, id: int) -> Optional[UserModel]:
        with get_db() as db:
            user = db.query(User).filter(User.id == id).first()
            if user:
                return UserModel.model_validate(user)
            else:
                return None


Users = UserTable()
