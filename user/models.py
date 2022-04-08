from django.db import models
from django.forms import CharField

# Create your models here.
class User(models.Model):
    username = models.CharField('用户名',max_length=30,unique=True)
    password = models.CharField('密码',max_length=32)
    created_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)

    def __str__(self):
        return f'用户：{self.username},密码：{self.password}'

    class Meta:
        db_table = 'User'