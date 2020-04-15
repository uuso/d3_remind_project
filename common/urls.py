from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, RegisterView, CreateUserProfile
# from .views import index, loginv, logoutv

app_name = "common"

urlpatterns = [
    path("", index, name="index"),
    path("login/", LoginView.as_view(template_name='common/login.html'), name="login"),  # CBV
    path("logout/", LogoutView.as_view(), name="logout"),  # CBV
    path("register/", RegisterView.as_view(), name="register"),  # CBV
    path('profile-create/', CreateUserProfile.as_view(), name='profile-create'),
    # path("login/", loginv, name="login"), # self-created view
    # path("logout/", logoutv, name="logout"), # self-created view
]
