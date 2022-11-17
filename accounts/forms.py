from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.forms import ModelForm
from django import forms
from django.contrib.auth.hashers import check_password


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "nickname", "age")
        labels = {
            "nickname": "닉네임",
        }

    def signup(self, request, user):
        # form에 기입된 데이터를 가져오기 위해 cleaned_data 사용
        user.nickname = self.cleaned_data["nickname"]
        user.save()


class ProfileForm(ModelForm):
    class Meta:
        model = Profile()
        fields = ["intro", "image"]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["nickname"]
        labels = {
            "nickname": "닉네임",
        }


# 비밀번호 확인
class CheckPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = self.user.password
        if password:
            if not check_password(password, confirm_password):
                self.add_error("password", "비밀번호가 달라요.")
