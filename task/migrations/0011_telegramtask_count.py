# Generated by Django 3.2 on 2022-05-01 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0010_alter_telegramaccount_tid'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramtask',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]