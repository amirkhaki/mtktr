from django.db import models
from django.contrib.auth import get_user_model


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class TelegramTask(models.Model):
    creator = models.ForeignKey(get_user_model(), 
            related_name='tg_tasks',
            on_delete=models.CASCADE)
    # cost per perform
    cpp = models.PositiveIntegerField(verbose_name='cost per perform')
    types = (('group', 'Group'), ('channel', 'Channel'))
    task_type = models.CharField(max_length=10, choices=types)
    
class TelegramAccount(models.Model):
    owner = models.ForeignKey(get_user_model(), 
            related_name='tg_accounts',
            on_delete=models.SET(get_sentinel_user) )
    verified = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=32)
    # user id in telegram
    tid = models.CharField(unique=True, max_length=30,
            verbose_name='telegram id')
    tasks = models.ManyToManyField(TelegramTask,
            blank=True, related_name='performers')


    def verify(self):
        """
        verify will set verified true if account meets several conditions
        """
        pass

    def __str__(self):
        return self.username

