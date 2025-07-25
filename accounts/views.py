from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm, LoginForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "accounts/register.html"

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data["phone"], random_code)
            OtpCode.objects.create(
                phone_number=form.cleaned_data["phone"], code=random_code
            )
            request.session["user_registration_info"] = {
                "phone_number": form.cleaned_data["phone"],
                "email": form.cleaned_data["email"],
                "full_name": form.cleaned_data["full_name"],
                "password": form.cleaned_data["password"],
            }
            messages.success(request, "we send for yoy a code", "success")
            return redirect("accounts:verify_code")
        return render(request, self.template_name, {"form": form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_registration_info"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if code_instance.code == cd["code"]:
                print("*" * 90)
                print(user_session)
                User.objects.create(
                    email=user_session["email"],
                    phone_number=user_session["phone_number"],
                    full_name=user_session["full_name"],
                    password=user_session["password"],
                )
                code_instance.delete()
                messages.success(request, "you registred", "success")
                return redirect("home:home")
            else:
                messages.error(request, "this code is wrong", "danger")
                return redirect("accounts:verify_code")
        return redirect("home:home")


class LoginView(View):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "با موفقیت وارد شدید.", "success")
                return redirect("home:home")
            else:
                messages.error(request, "نام کاربری یا رمز عبور اشتباه است.", "warning")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home:home")
