# Generated by Django 3.2 on 2022-04-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_auto_20220419_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramtask',
            name='cpp',
            field=models.PositiveIntegerField(verbose_name='cost per perform'),
        ),
    ]