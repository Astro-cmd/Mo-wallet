from django.db import models
from django.utils.timezone import now

class MpesaTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('C2B', 'Customer to Business'),
        ('B2C', 'Business to Customer'),
        ('B2B', 'Business to Business'),
    )

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    account_reference = models.CharField(max_length=100, blank=True, null=True)
    transaction_description = models.TextField(blank=True, null=True)
    organization_balance = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    transaction_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.transaction_id} - {self.amount}"
