from django.db import models
from main.models import Region
from django.conf import settings

# Create your models here.
class Photospot(models.Model):
    content = models.TextField()
    photo_img = models.ImageField(upload_to="images/%Y/%m/%d", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_photospots"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # region = models.ForeignKey(Region, on_delete=models.CASCADE)
