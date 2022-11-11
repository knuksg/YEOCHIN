from django import forms
from .models import Photospot, Photocomment


class PhotospotForm(forms.ModelForm):
    class Meta:
        model = Photospot
        fields = [
            "place",
            "photo_img",
            "content",
        ]
        labels = {
            "place": "장소",
            "photo_img": "인생사진",
            "content": "이야기",
        }
        widgets = {"content": forms.Textarea(attrs={"placeholder": "자유롭게 작성해 주세요 :)"})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Photocomment
        fields = [
            "content",
        ]
        labels = {
            "content": "",
        }
