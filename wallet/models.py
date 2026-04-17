from django.db import models
from users.models import User
from budget.models import Budget
from goals.models import SavingsGoal
from django.utils import timezone
from datetime import timedelta

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class Prediction(models.Model):
    PREDICTION_TYPE_CHOICES = [
        ('budget', 'Budget'),
        ('goal', 'Goal'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    prediction_type = models.CharField(max_length=10, choices=PREDICTION_TYPE_CHOICES)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, blank=True, related_name='predictions')
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, null=True, blank=True, related_name='predictions')
    predicted_value = models.DecimalField(max_digits=12, decimal_places=2)
    prediction_date = models.DateField(auto_now_add=True)
    target_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, achieved, failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prediction for {self.user.username} ({self.prediction_type}) on {self.target_date}"


class PaymentMethod(models.Model):
    CARD_TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    card_number = models.CharField(max_length=20)  # Last 4 digits or masked
    cardholder_name = models.CharField(max_length=100)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.card_type} - {self.card_number[-4:]}"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    issue_date = models.DateField(auto_now_add=True)
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.amount}"

    @property
    def is_overdue(self):
        if self.status == 'paid':
            return False
        return self.due_date < timezone.now().date()

    @property
    def days_until_due(self):
        if self.paid_date:
            return 0
        delta = self.due_date - timezone.now().date()
        return max(0, delta.days)


class Bill(models.Model):
    CATEGORY_CHOICES = [
        ('utilities', 'Utilities'),
        ('subscriptions', 'Subscriptions'),
        ('insurance', 'Insurance'),
        ('rent', 'Rent'),
        ('taxes', 'Taxes'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bills')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    paid_date = models.DateField(null=True, blank=True)
    recurring = models.BooleanField(default=False)  # Monthly, yearly, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.name} - {self.amount}"

    @property
    def is_overdue(self):
        if self.is_paid:
            return False
        return self.due_date < timezone.now().date()
