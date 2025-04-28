from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from users.models import User
from decimal import Decimal
from transactions.models import Transaction

class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    goal_name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    @property
    def progress(self):
        return (self.current_savings / self.target_amount) * 100 if self.target_amount > 0 else 0
    
    @property
    def remaining_amount(self):
        return self.target_amount - self.current_savings
    
    @property
    def is_achievable(self):
        """Check if the goal is still achievable by the deadline."""
        if self.completed:
            return True
        
        days_left = (self.deadline - timezone.now().date()).days
        if days_left <= 0:
            return False
        
        required_daily_savings = self.remaining_amount / days_left if days_left > 0 else 0
        return required_daily_savings <= self.user.wallet.balance
    
    @property
    def days_left(self):
        return max(0, (self.deadline - timezone.now().date()).days)
    
    def add_contribution(self, amount):
        """Add a contribution to the goal and update current savings."""
        if amount <= 0:
            raise ValidationError("Contribution amount must be positive.")
        
        contribution = GoalContribution.objects.create(
            goal=self,
            amount=amount
        )
        
        self.current_savings += amount
        if self.current_savings >= self.target_amount:
            self.completed = True
        self.save()
        
        return contribution
    
    def can_delete(self):
        """Check if the goal can be safely deleted."""
        return not self.completed and self.current_savings == 0
    
    def clean(self):
        if self.deadline and self.deadline < timezone.now().date():
            raise ValidationError("Deadline must be in the future.")
        if self.current_savings > self.target_amount:
            raise ValidationError("Current savings cannot exceed target amount.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.goal_name} ({self.user.username})"

class GoalContribution(models.Model):
    goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True, related_name='goal_contribution')
    
    class Meta:
        ordering = ['-date']
    
    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Contribution amount must be positive.")
        
        if self.goal.completed:
            raise ValidationError("Cannot contribute to a completed goal.")

        # Validate that user has sufficient wallet balance
        if self.goal.user.wallet.balance < self.amount:
            raise ValidationError("Insufficient funds in wallet.")
    
    def save(self, *args, **kwargs):
        self.clean()
        
        # Create transaction if it doesn't exist
        if not self.transaction and not kwargs.pop('skip_transaction', False):
            from transactions.models import Transaction
            self.transaction = Transaction.objects.create(
                user=self.goal.user,
                amount=self.amount,
                category='savings',
                payment_method='wallet',
                transaction_type='expense',
                description=f'Contribution to savings goal: {self.goal.goal_name}'
            )
            
            # Update wallet balance
            wallet = self.goal.user.wallet
            wallet.balance -= self.amount
            wallet.save()
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Reverse the transaction if it exists
        if self.transaction:
            wallet = self.goal.user.wallet
            wallet.balance += self.amount
            wallet.save()
            self.transaction.delete()
        
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.goal.goal_name} - {self.amount} on {self.date.strftime('%Y-%m-%d')}"
