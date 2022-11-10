from django.db import models
import datetime

# Create your models here.
class Friend(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateField()
    end_at = models.DateField(null=True)

class Friend_Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
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
