from django.db import models
from user.models import UserProfile
from topic.models import Topic


# Create your models here.
class Message(models.Model):
    content = models.CharField(verbose_name='留言内容', max_length=50)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='留言创建时间')
    parent_message = models.IntegerField(verbose_name='父留言ID', default=0)
    publisher = models.ForeignKey(UserProfile)
    topic = models.ForeignKey(Topic)

    class Meta:
        db_table = 'message'
