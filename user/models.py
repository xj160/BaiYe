from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from . import until
from BaiYe import settings
import random
from system.storage import ImageStorage
import os
# Create your models here.
class UserProfile(AbstractUser):
    uid = models.AutoField(verbose_name='uid',primary_key=True)
    nick_name = models.CharField(verbose_name='昵称',max_length=50)
    icon = models.ImageField(verbose_name='头像',upload_to='up_load/',blank=True)
    phone = models.CharField(verbose_name='手机号码',max_length=11,unique=True)
    register_time = models.DateTimeField(verbose_name='注册时间',default=timezone.now)
    register_ip = models.CharField(verbose_name='注册IP',max_length=15)
    # STATUS_TYPE = [('online','在线'),('offline','离线')]
    # statu =
    # is_active = models.BooleanField(
    #     verbose_name='活跃',
    #     default=True,
    #     help_text=(
    #         'Designates whether this user should be treated as active. '
    #         'Unselect this instead of deleting accounts.'
    #     ),
    # )

    def save(self, *args, **kwargs):
        name = str(self.icon)
        if self.icon:
            if 'default' not in name:
                icon_url = 'User/' + self.username + '/'
                # if self.icon and icon_path not in str(self.icon):
                #     icon_name = until.get_icon_name()
                icon = until.save_image(self.icon.file,icon_url,name)
                if icon:
                    self.icon =icon.replace('\\','/')

        else:
            default_icon_dir = os.path.join(settings.MEDIA_ROOT,'default_icon')
            default_icon = random.choice(os.listdir(default_icon_dir))
            icon = os.path.join(default_icon_dir.split('media\\')[-1], default_icon)
            icon.replace('\\','/')
            self.icon = icon.replace('\\', '/')

        super().save(*args, **kwargs)

        # self.password = until.toMD5(self.password)
        # username = until.uuid(self.password)
    #     while UserProfile.objects.filter(username=username) == []:
    #         username = until.uuid(self.password)
    #     self.username = username
    #     super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     # print('icon:',self.icon)
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'userprofile'