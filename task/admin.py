from django.contrib import admin
from .models import TelegramAccount, TelegramTask, DiscordAccount, DiscordTask
# Register your models here.


admin.site.register(TelegramTask)
admin.site.register(TelegramAccount)
admin.site.register(DiscordTask)
admin.site.register(DiscordAccount)

