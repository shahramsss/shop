from django import forms
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور"}
        ),
    )
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "phone_number", "full_name"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password2"] and cd["password1"] != cd["password2"]:
            raise ValidationError("رمز عبور و تکرار رمز عبور برابر نیستند!")
        return cd["password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password">this form</a>'
    )

    class Meta:
        model = User
        fields = ["email", "phone_number", "full_name", "password", "last_login"]


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل"}
        ),
    )
    full_name = forms.CharField(
        label="نام و نام خانوادگی",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی"}
        ),
    )
    phone = forms.CharField(
        label="موبایل",
        max_length=11,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "موبایل"}
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور"}
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("این ایمیل وجود دارد!")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError("این موبایل وجود دارد!")
        return phone


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(
        label="کد",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "کد رسال شده"}
        ),
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        max_length=155,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام کاربری"}
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور"}
        ),
    )
