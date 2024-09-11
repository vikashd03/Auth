from .handlers import handle_error
from .serializers import UserDataSerializer, UserSerializer
from .models import User


class UserTable:
    @handle_error()
    def get_user_by_email(email: str):
        user = User.objects.get(email=email)
        user_data = UserSerializer(user).data
        return user_data

    @handle_error()
    def insert_user(
        email: str,
        username: str,
        password: str,
    ):
        user_data = {
            "email": email,
            "name": username,
            "password": password,
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return user_serializer.data
        else:
            return None

    @handle_error()
    def get_user_by_id(id: int):
        user = User.objects.get(id=id)
        user_data = UserDataSerializer(user).data
        return user_data

    @handle_error()
    def get_all_users():
        users = User.objects.all().order_by("id")
        user_data = UserDataSerializer(users, many=True).data
        return user_data

    @handle_error()
    def update_email_by_id(id: int, email: str):
        user_serializer = UserSerializer(
            instance=User.objects.get(id=id), data={"email": email}, partial=True
        )
        if user_serializer.is_valid():
            user_serializer.save()
            return user_serializer.data
        else:
            return None
    
    @handle_error()
    def update_username_by_id(id: int, name: str):
        user_serializer = UserSerializer(
            instance=User.objects.get(id=id), data={"name": name}, partial=True
        )
        if user_serializer.is_valid():
            user_serializer.save()
            return user_serializer.data
        else:
            return None

    @handle_error()
    def update_password_by_id(id: int, password: str):
        user_serializer = UserSerializer(
            instance=User.objects.get(id=id), data={"password": password}, partial=True
        )
        if user_serializer.is_valid():
            user_serializer.save()
            return user_serializer.data
        else:
            return None
