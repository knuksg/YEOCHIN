from django import forms
from .models import Friend, Friend_Comment, FriendRequest


class DateInput(forms.DateInput):
    input_type = "date"


class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = [
            "title",
            "content",
            "start_at",
            "end_at",
            "place",
            "people_number",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "제목을 작성해 해주세요"}),
            "content": forms.Textarea(
                attrs={"placeholder": "자유롭게 작성해 주세요(ex. 동행 계획, 여행 스타일 등)"}
            ),
            "start_at": DateInput(),
            "end_at": DateInput(),
            "place": forms.TextInput(attrs={"placeholder": "원하는 동행 장소를 작성해 주세요"}),
            "people_number": forms.NumberInput(
                attrs={"placeholder": "원하는 동행 인원을 작성해 주세요"}
            ),
        }
        labels = {
            "title": "제목",
            "content": "내용",
            "start_at": "시작날짜",
            "end_at": "마감날짜",
            "place": "장소",
            "people_number": "인원",
            "image": "이미지",
        }


class Friend_CommentForm(forms.ModelForm):
    class Meta:
        model = Friend_Comment
        fields = ["content"]

        labels = {
             "content": "댓글",
        }

from chats.models import Room

class FriendRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'users',]
