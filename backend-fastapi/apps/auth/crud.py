from typing import List, Optional

from .models import User
from .schemas import UserModel
from internal.db import get_db


class UserTable:
    def create_user(self, name: str, email: str, passowrd: str) -> Optional[UserModel]:
        with get_db() as db:
            user = User(**{"name": name, "email": email, "password": passowrd})
            db.add(user)
            db.commit()
            db.refresh(user)
            if user:
                return UserModel.model_validate(user)
            else:
                return None

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

    def get_all_users(self) -> Optional[List[UserModel]]:
        with get_db() as db:
            users = db.query(User).all()
            if users:
                return users
            else:
                return []

    def update_name(self, id, name) -> UserModel:
        with get_db() as db:
            user = db.query(User).filter(User.id == id).first()
            user.name = name
            db.commit()
            db.refresh(user)
            if user:
                return UserModel.model_validate(user)
            else:
                return None


Users = UserTable()
