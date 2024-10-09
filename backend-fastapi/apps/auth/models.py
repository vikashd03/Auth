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
    is_active = Column(Boolean, default=True)


class UserBase(BaseModel):
    email: str
    name: str


class UserCreate(UserBase):
    password: str


class UserModel(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool


class UserTable:
    def create_user(self, name: str, email: str, password: str) -> Optional[UserModel]:
        with get_db() as db:
            user = User(**{"name": name, "email": email, "password": password})
            db.add(user)
            db.commit()
            db.refresh(user)
            return user


Users = UserTable()
