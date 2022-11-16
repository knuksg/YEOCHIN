from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Photospot(models.Model):
    place = models.CharField(max_length=30)
    content = models.TextField()
    photo_img = models.ImageField(upload_to="images/%Y/%m/%d", blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_photospots"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hits = models.IntegerField(default=0)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + "일 전"
        else:
            return False


    def get_absolute_url(self):
        return reverse("qna:detail", args=[self.pk])
    
class Photocomment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photospot = models.ForeignKey(Photospot, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
