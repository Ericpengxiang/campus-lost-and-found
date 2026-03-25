from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', '学生'),
        ('staff', '教职工'),
    ]
    phone = models.CharField('手机号', max_length=20, blank=True, null=True)
    student_id = models.CharField('学号/工号', max_length=32, blank=True, null=True)
    department = models.CharField('院系/部门', max_length=128, blank=True, null=True)
    user_type = models.CharField('用户类型', max_length=10, choices=USER_TYPE_CHOICES, default='student')
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', blank=True, null=True)
    created_at = models.DateTimeField('注册时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = 'users_user'

    def __str__(self):
        return self.username

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
