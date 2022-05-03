from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string as random


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class TelegramTask(models.Model):
    # cost per perform
    cpp = models.PositiveIntegerField(verbose_name='cost per perform')
    types = (('group', 'Group'), ('channel', 'Channel'))
    task_type = models.CharField(max_length=10, choices=types)
    chat_id = models.CharField(max_length=33, default='telegram')
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.chat_id + f' ({self.count})'
    
class TelegramAccount(models.Model):
    owner = models.ForeignKey(get_user_model(), 
            related_name='tg_accounts',
            on_delete=models.SET(get_sentinel_user) )
    verified = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=32)
    # user id in telegram
    tid = models.BigIntegerField(unique=True,
            verbose_name='telegram id', null=True)
    tasks = models.ManyToManyField(TelegramTask,
            blank=True, related_name='performers')
    token = models.CharField(max_length=20, editable=False, default=random )


    def __str__(self):
        return self.username + '@' + self.owner.username

