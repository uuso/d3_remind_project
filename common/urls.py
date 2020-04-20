from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, RegisterView, CreateUserProfileView


app_name = "common"

urlpatterns = [
    path("", index, name="index"),
    path("user/login/", LoginView.as_view(), name="user-login"),
    path("user/logout/", LogoutView.as_view(), name="user-logout"),
    path("user/register/", RegisterView.as_view(), name="user-register"),
    path('profile/create/', CreateUserProfileView.as_view(), name='profile-create'),
]
