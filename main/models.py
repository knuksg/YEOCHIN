from django.db import models

# Create your models here.
class Region(models.Model):
    name = models.CharField(max_length=10)

class DetailRegion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)