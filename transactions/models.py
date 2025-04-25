from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from users.models import User
from decimal import Decimal
from core.categories import TRANSACTION_CATEGORIES

class Transaction(models.Model):
    TRANSACTION_CATEGORIES = TRANSACTION_CATEGORIES
    PAYMENT_METHODS = [
        ('wallet', 'Wallet'),
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('other', 'Other')
    ]
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)  # Keep this for record creation time
    transaction_date = models.DateTimeField(auto_now_add=True)  # Changed to auto_now_add
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['user', '-date']),
        ]

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Transaction amount must be positive.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} - {self.category}"

@receiver(pre_save, sender=Transaction)
def add_category_if_not_exists(sender, instance, **kwargs):
    """Add new categories to TRANSACTION_CATEGORIES if they don't exist."""
    if instance.category not in dict(Transaction.TRANSACTION_CATEGORIES):
        Transaction.TRANSACTION_CATEGORIES += ((instance.category, instance.category.capitalize()),)