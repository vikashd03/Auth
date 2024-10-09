from fastapi import FastAPI

from internal.utils import register_validation_exception_handler
from .models import UserCreate, UserModel, Users

app = FastAPI()

register_validation_exception_handler(app)


@app.post("/signup", response_model=UserModel)
async def signup(form_data: UserCreate):
    user = Users.create_user(**form_data.model_dump())
    if user:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
        }
