import uuid
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


def generate_account_number():
    return str(uuid.uuid4().hex)[:10] # generate a unique 10-character account number using UUID

class Account(models.Model):
    currency_choices = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(default=generate_account_number, max_length=10, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    currency = models.CharField(max_length=3, choices=currency_choices)
    is_active = models.BooleanField(default=True)