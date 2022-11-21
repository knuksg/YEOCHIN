from django import forms
from .models import *
from tag.models import *
# from django_summernote.widgets import SummernoteWidget


class QnaForm(forms.ModelForm):
    class Meta:
        model = Qna
        fields = [
            "title",
            "content",
            "image",
            "tag",
            "region",
        ]
        # widgets = {
        #     'content': SummernoteWidget(),
        # }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = [
            "content",
        ]