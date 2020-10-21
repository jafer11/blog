from django.db import models


# Create your models here.

# class -> UserProfile
# 表名 user_profile
# username, nickname, email, password, sign, info, avatar

class UserProfile(models.Model):
    username = models.CharField(verbose_name='用户名',
                                max_length=11,
                                primary_key=True
                                )
    nickname = models.CharField(verbose_name='昵称',
                                max_length=30
                                )
    email = models.CharField(verbose_name='邮箱',
                             max_length=50,
                             null=True
                             )
    password = models.CharField(verbose_name='密码',
                                max_length=32
                                )
    sign = models.CharField(verbose_name='个性签名',
                            max_length=50)
    info = models.CharField(verbose_name='个人描述',
                            max_length=150
                            )
    avatar = models.ImageField(upload_to='avatar/')

    # 改表名
    class Meta:
        db_table = 'user_profile'
