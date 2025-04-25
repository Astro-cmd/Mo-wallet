from django.db import models
from users.models import User
from transactions.models import Transaction
from core import categories
from django.utils import timezone

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=50, choices=categories.TRANSACTION_CATEGORIES)
    limit = models.DecimalField(max_digits=12, decimal_places=2)  # renamed from monthly_limit
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def remaining(self):
        return self.limit - self.amount_spent
    
    @property
    def percentage_used(self):
        if self.limit and self.limit > 0:
            return (self.amount_spent / self.limit) * 100
        return 0
    
    def __str__(self):
        return f"{self.get_category_display()} budget ({self.user.username})"

