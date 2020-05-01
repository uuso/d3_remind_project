from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from allauth.account.views import login, logout

from . import views


app_name = "common"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/socials/", login, name="user-login-socials"),
    path("logout/socials/", logout, name="user-logout-socials"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("register/", views.RegisterView.as_view(), name="user-register"),
    path('info/', views.UserInfoView.as_view(), name="user-info"),
]
