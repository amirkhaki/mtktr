# Generated by Django 3.2 on 2022-04-20 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_alter_telegramtask_cpp'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramtask',
            name='url',
            field=models.URLField(default='https://t.me/telegram'),
        ),
    ]
