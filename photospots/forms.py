from django import forms
from .models import Photospot, Photocomment


class PhotospotForm(forms.ModelForm):
    class Meta:
        model = Photospot
        fields = [
            "photo_img",
            "place",
            "content",
        ]
        labels = {
            "photo_img": "인생사진",
            "place": "포토스팟",
            "content": "이야기",
        }
        widgets = {
            "place": forms.TextInput(attrs={"placeholder": "포토스팟 위치를 공유해주세요"}),
            "content": forms.Textarea(attrs={"placeholder": "자유롭게 작성해 주세요"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Photocomment
        fields = [
            "content",
        ]
        labels = {
            "content": "",
        }
