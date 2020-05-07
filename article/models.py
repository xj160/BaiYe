from django.db import models
from user.models import UserProfile
# Create your models here.
import time
from django.utils import timezone

class Anthology(models.Model):
    name = models.CharField(verbose_name='文集名称',max_length=100)
    date = models.DateTimeField(verbose_name='注册时间',default=timezone.now())
    user = models.ForeignKey(to=UserProfile, verbose_name='用户', on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     if not Article.objects.filter(anthology=self):
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'Anthology'

class Article(models.Model):
    anthology = models.ForeignKey(to=Anthology,verbose_name='文集',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题',max_length=100)
    content = models.TextField(verbose_name='内容')
    is_public = models.BooleanField(default=False)
    date = models.DateTimeField(verbose_name='创建时间',default=timezone.now())
    last_edit = models.DateTimeField(verbose_name='上次编辑',auto_now=True)
    click_num = models.IntegerField(default=0,verbose_name='点击量')
    love_num = models.IntegerField(default=0,verbose_name='点赞量')
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'Article'