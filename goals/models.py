from django.db import models
from users.models import User
class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    goal_name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    @property
    def progress(self):
        return (self.current_savings / self.target_amount) * 100 if self.target_amount > 0 else 0
    
    def __str__(self):
        return f"{self.goal_name} ({self.user.username})"
