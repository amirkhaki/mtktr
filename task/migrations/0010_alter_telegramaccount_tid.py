# Generated by Django 3.2 on 2022-04-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_telegramaccount_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramaccount',
            name='tid',
            field=models.BigIntegerField(null=True, unique=True, verbose_name='telegram id'),
        ),
    ]
