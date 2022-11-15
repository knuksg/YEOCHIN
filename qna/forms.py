from django import forms
from .models import *

class QnaForm(forms.ModelForm):
    class Meta:
        model = Qna
        fields = [
            "title",
            "content",
            "image",
            "tag"
        ]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            "content",
        ]