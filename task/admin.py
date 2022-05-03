from django.contrib import admin
from .models import TelegramAccount, TelegramTask
# Register your models here.


admin.site.register(TelegramTask)
admin.site.register(TelegramAccount)
