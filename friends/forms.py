from django import forms
from .models import Friend, Friend_Comment


class QnaForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "image",
        ]


class QnaCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]


