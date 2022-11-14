from django import forms
from .models import Hotel, HotelReview
from django_summernote.widgets import SummernoteWidget

class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ['rating', 'title', 'content']
        labels = {
            'rating': '별점',
            'title': '제목',
            'content': '',
        }
        widgets = {
            'content': SummernoteWidget(),
        }