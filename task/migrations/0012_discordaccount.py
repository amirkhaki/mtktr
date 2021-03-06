# Generated by Django 3.2 on 2022-05-03 18:37

from django.conf import settings
from django.db import migrations, models
import task.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0011_telegramtask_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('did', models.BigIntegerField(unique=True, verbose_name='discord id')),
                ('access_token', models.CharField(max_length=100)),
                ('refresh_token', models.CharField(max_length=100)),
                ('expire_date', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=models.SET(task.models.get_sentinel_user), related_name='dc_accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
