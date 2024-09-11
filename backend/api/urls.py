from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
    path("users/", views.get_users, name="get all users"),
    path("user/", views.get_user, name="get user data"),
    path("update/email/", views.update_email, name="update email"),
    path("update/username/", views.update_username, name="update user name"),
    path("update/password/", views.update_password, name="udpate password"),
    path("refresh/token/", views.refresh_token, name="refresh token"),
]
