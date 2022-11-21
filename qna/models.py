
from datetime import datetime, timedelta, timezone
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.

class Qna(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/%Y/%m/%d", blank=True)
    hits = models.PositiveIntegerField(default=0)
    closed = models.BooleanField(default=False)
    region = models.TextField()
    place = models.CharField(max_length=30)
    like_users = models.ManyToManyField(
    settings.AUTH_USER_MODEL, related_name="like_qna"
    )
    tag = models.ManyToManyField('tag.Tag', blank=True, verbose_name = "태그")
    
    @property
    def qna_answers(self):
        answers = Answer.objects.filter(qna=self)
        if len(answers) == 0:
            return 0
        else:
            return len(answers)
        
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = "qna_board"
        verbose_name = "qna"
        verbose_name_plural = "qna"  
        
    
    def get_absolute_url(self):
        return reverse("qna:detail", args=[self.pk])  
    
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
        
        
    @property
    def click(self):
        self.hits += 1
        self.save()

    @property
    def full_name(self):
        return f"{self.last_name}{self.first_name}"


# class Category(models.Model):
#     name = models.CharField(max_length=20, db_index=True)
#     meta_description = models.TextField(blank=True)
#     slug = models.SlugField(
#         max_length=20, db_index=True, unique=True, allow_unicode=True
#     )

#     class Meta:
#         ordering = ["name"]
#         verbose_name = "category"
#         verbose_name_plural = "categories"

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("articles:article_in_category", args=[self.slug])

class Answer(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    qna = models.ForeignKey(Qna, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return "방금 전"
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + "분 전"
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + "시간 전"
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + "일 전"
        else:
            return False
