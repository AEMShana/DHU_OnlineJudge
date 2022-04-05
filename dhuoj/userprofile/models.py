from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    # 与 User 模型构成一对一的关系
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    # 电话号码字段
    phone = models.CharField(max_length=20, blank=True)
    # 头像
    photo = models.ImageField(upload_to='photo/%Y%m%d/', blank=True)
    # 个人简介
    bio = models.TextField(max_length=500, blank=True)
    # 邮箱
    email = models.TextField(max_length=50, blank=True)
    # 专业班级
    major = models.TextField(max_length=50, blank=True)

    realName = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)
