from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from django.conf import settings
from django import forms
from django.contrib.auth.hashers import check_password



# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True, null=True)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    pass


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    intro = models.TextField(blank=True)  # 소개글
    image = ProcessedImageField(
        blank=True,
        upload_to="profile/",
        processors=[Thumbnail(300, 300)],
        format="JPEG",
        options={"quality": 60},
    )
    
# 비밀번호 확인
class CheckPasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput())
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password
        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 달라요.')
