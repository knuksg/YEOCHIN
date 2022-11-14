from django.db import models
from django.conf import settings

# Create your models here.
class Photospot(models.Model):
    place = models.CharField(max_length=30)
    content = models.TextField()
    photo_img = models.ImageField(upload_to="images/%Y/%m/%d", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_photospots"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hits = models.PositiveBigIntegerField(default=0, verbose_name="조회수")


class Photocomment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photospot = models.ForeignKey(Photospot, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
