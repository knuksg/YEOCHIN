from .models import Hotel, HotelReview
from django import forms

class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ['rating', 'title', 'content']