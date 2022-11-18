from django.db import models

#Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name="태그명")
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "qna_tag"
        verbose_name = "태그"
        verbose_name_plural = "태그"
        