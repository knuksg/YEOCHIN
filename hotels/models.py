from django.db import models
from main.models import Region, DetailRegion

# Create your models here.
class Hotel(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    detail_region = models.ForeignKey(DetailRegion, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    url = models.TextField()
    rating = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)
    price = models.CharField(max_length=10)
    address = models.TextField()
    facilities = models.TextField()
    image = models.TextField()