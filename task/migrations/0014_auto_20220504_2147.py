# Generated by Django 3.2 on 2022-05-04 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_auto_20220504_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscordTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guild_name', models.CharField(max_length=200)),
                ('guild_id', models.CharField(max_length=200)),
                ('cpp', models.PositiveIntegerField(verbose_name='cost per perform')),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='discordaccount',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='performers', to='task.DiscordTask'),
        ),
    ]
