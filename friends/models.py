from django.db import models
from datetime import timedelta , datetime, timezone 
from django.contrib.auth import get_user_model


# Create your models here.
class Friend(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateField()
    end_at = models.DateField(null=True)
    place = models.CharField(max_length=30)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like_user = models.ManyToManyField(get_user_model(), related_name="like_friend")
    people_number = models.IntegerField()

    image = models.ImageField(upload_to="image/", blank=True)
    hits = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)

class Friend_Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    friend =  models.ForeignKey(Friend, on_delete=models.CASCADE)
    
    
    
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

from accounts.models import User

class FriendRequest(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requests')