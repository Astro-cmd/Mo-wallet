from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from transactions.models import Transaction
from .models import Budget

@receiver([post_save, post_delete], sender=Transaction)
def update_budget_on_transaction_change(sender, instance, **kwargs):
    """
    Update budget amounts when transactions are created, modified, or deleted
    """
    if instance.transaction_type == 'expense':  # Only track expenses for budgets
        # Get the current month's budget for this category
        current_month = timezone.now().month
        current_year = timezone.now().year
        try:
            budget = Budget.objects.get(
                user=instance.user,
                category=instance.category
            )
            
            # Calculate total spent in this category for current month
            total_spent = Transaction.objects.filter(
                user=instance.user,
                category=instance.category,
                transaction_type='expense',
                transaction_date__month=current_month,
                transaction_date__year=current_year
            ).exclude(id=instance.id if kwargs.get('created', False) else None)\
             .aggregate(total=models.Sum('amount'))['total'] or 0
            
            budget.amount_spent = total_spent
            budget.save()
        except Budget.DoesNotExist:
            pass  # No budget set for this category