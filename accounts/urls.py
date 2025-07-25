from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("verifycode/", views.UserRegisterVerifyCodeView.as_view(), name="verify_code"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
