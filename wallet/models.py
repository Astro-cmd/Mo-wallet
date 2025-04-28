from django.db import models
from users.models import User
from budget.models import Budget
from goals.models import SavingsGoal

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
