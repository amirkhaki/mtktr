from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    credit = models.IntegerField(default=0)

class Withdrawal(models.Model):
    user = models.ForeignKey(get_user_model(), 
            related_name='withdrawals', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    address = models.CharField(max_length=500)
    statuses = (
            ('p', 'Pending'),
            ('a', 'Approved')
            )
    status = models.CharField(max_length=10, choices=statuses, default='p')
    message = models.TextField(max_length=1000)


    def __str__(self):
        return f'{self.user} {self.amount}'


