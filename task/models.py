from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string as random
from django.conf import settings
import datetime
import requests

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class DiscordTask(models.Model):
    guild_name = models.CharField(max_length=200)
    guild_id = models.CharField(unique=True, max_length=200)
    cpp = models.PositiveIntegerField(verbose_name='cost per perform')
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.guild_name + f' ({self.count})'
    

class DiscordAccount(models.Model):
    owner = models.ForeignKey(get_user_model(), 
            related_name='dc_accounts',
            on_delete=models.SET(get_sentinel_user) )
    # user id in discord
    did = models.CharField(max_length=100, unique=True, verbose_name = 'discord id' )
    access_token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)
    expire_date = models.DateTimeField()
    username = models.CharField(max_length=100, default='user#0000')
    tasks = models.ManyToManyField(DiscordTask,
            blank=True, related_name='performers')

    def is_expired(self):
        return self.expire_date <= datetime.datetime.now()
    def _exchange_code(self, code):
        data = {
                'client_id': settings.DC_OAUTH2_CLIENT_ID,
                'client_secret': settings.DC_OAUTH2_CLIENT_SECRET,
                'grant_type': 'refresh_token',
                'code': self.refresh_token,
                'redirect_uri': settings.DC_OAUTH2_REDIRECT_URI
                }
        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
                }
        r = requests.post(settings.DC_TOKEN_URL, data=data, headers=headers)
        r.raise_for_status()
        token = r.json()
        self.access_token = token['access_token']
        exp_date = datetime.datetime.now() + datetime.timedelta(seconds=token['expires_in']-4)
        self.expire_date = exp_date
        self.save()

    def __str__(self):
        return self.username




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
    tid = models.CharField(max_length=100, unique=True,
            verbose_name='telegram id', null=True)
    tasks = models.ManyToManyField(TelegramTask,
            blank=True, related_name='performers')
    token = models.CharField(max_length=20, editable=False, default=random )


    def __str__(self):
        return self.username + '@' + self.owner.username

