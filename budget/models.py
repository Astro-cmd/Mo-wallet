from django.db import models
from users.models import User
from transactions.models import Transaction
from core import categories

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.CharField(max_length=50, choices=categories.TRANSACTION_CATEGORIES)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def remaining(self):
        return self.monthly_limit - self.amount_spent
    
    def __str__(self):
        return f"{self.get_category_display()} budget ({self.user.username})"

