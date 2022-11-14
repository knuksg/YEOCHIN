from django.conf import settings
from django.db import models
from main.models import Region, DetailRegion
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Hotel(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    detail_region = models.ForeignKey(DetailRegion, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    url = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    grade = models.CharField(max_length=10)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    address = models.TextField()
    facilities = models.TextField()
    image = models.TextField()

    @property
    def user_rating(self):
        reviews = HotelReview.objects.filter(hotel=self)
        ratings = [self.rating]
        for review in reviews:
            ratings.append(review.rating)
        try:
            return round(sum(ratings) / len(ratings), 1)
        except: # 기존 평가도 없고 유저 평가도 없을 경우 0을 반환
            return 0

class HotelReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)