from django.contrib import admin
from django.contrib.auth import get_user_model as gum

admin.site.register(gum())

# Register your models here.
