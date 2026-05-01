"""
Signals to sync transactions with budgets.
When an expense transaction is created/updated, the corresponding budget's amount_spent is updated.
"""
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.db import transaction as db_transaction
from decimal import Decimal
from .models import Transaction
from budget.models import Budget


def get_transaction_difference(instance, old_amount=None, old_type=None, old_category=None):
    """
    Calculate the difference in amount for budget updates.
    
    Returns a tuple: (old_amount_for_budget, new_amount_for_budget)
    - Only considers expense transactions
    - Returns (0, 0) if transaction type is not 'expense'
    """
    # Old values (what should be removed from budget)
    if old_type == 'expense':
        old_budget_amount = old_amount or Decimal('0')
    else:
        old_budget_amount = Decimal('0')
    
    # New values (what should be added to budget)
    if instance.transaction_type == 'expense':
        new_budget_amount = instance.amount
    else:
        new_budget_amount = Decimal('0')
    
    return (old_budget_amount, new_budget_amount)


@receiver(pre_save, sender=Transaction)
def store_transaction_old_values(sender, instance, **kwargs):
    """
    Store old transaction values before save for comparison.
    This allows us to detect changes in amount or transaction type.
    """
    try:
        old_transaction = Transaction.objects.get(pk=instance.pk)
        instance._old_amount = old_transaction.amount
        instance._old_type = old_transaction.transaction_type
        instance._old_category = old_transaction.category
    except Transaction.DoesNotExist:
        # New transaction
        instance._old_amount = None
        instance._old_type = None
        instance._old_category = None


@receiver(post_save, sender=Transaction)
def sync_transaction_with_budget(sender, instance, created, **kwargs):
    """
    Sync transaction with budget when transaction is created or updated.
    
    - For new expense transactions: Add amount to matching budget
    - For updated transactions: 
      - If type changed from expense to non-expense: Subtract old amount from budget
      - If type changed from non-expense to expense: Add new amount to budget
      - If amount changed: Update budget with the difference
    """
    # Get old values (set in pre_save signal)
    old_amount = getattr(instance, '_old_amount', None)
    old_type = getattr(instance, '_old_type', None)
    old_category = getattr(instance, '_old_category', None)
    
    # Get budget amounts
    old_budget_amount, new_budget_amount = get_transaction_difference(
        instance, old_amount, old_type, old_category
    )
    
    # If nothing changed in terms of budget impact, skip
    if old_budget_amount == new_budget_amount and not created:
        return
    
    try:
        with db_transaction.atomic():
            # Handle category changes
            if old_category and old_category != instance.category and old_type == 'expense':
                # Remove old amount from old category budget if it was expense
                old_budget = Budget.objects.select_for_update().filter(
                    user=instance.user,
                    category=old_category
                ).first()
                
                if old_budget:
                    old_budget.amount_spent = max(
                        old_budget.amount_spent - old_amount,
                        Decimal('0')
                    )
                    old_budget.save()
            
            # Handle new budget for current category
            budget = Budget.objects.select_for_update().filter(
                user=instance.user,
                category=instance.category
            ).first()
            
            if budget and instance.transaction_type == 'expense':
                # Calculate the difference
                amount_difference = new_budget_amount - old_budget_amount
                budget.amount_spent = max(
                    budget.amount_spent + amount_difference,
                    Decimal('0')
                )
                budget.save()
            elif budget and old_type == 'expense' and instance.transaction_type != 'expense':
                # Transaction changed from expense to non-expense
                budget.amount_spent = max(
                    budget.amount_spent - old_budget_amount,
                    Decimal('0')
                )
                budget.save()
    
    except Budget.DoesNotExist:
        # Budget doesn't exist for this category, skip
        pass
    except Exception as e:
        print(f"Error syncing transaction with budget: {str(e)}")


@receiver(post_delete, sender=Transaction)
def remove_transaction_from_budget(sender, instance, **kwargs):
    """
    Remove transaction amount from budget when transaction is deleted.
    Only applies to expense transactions.
    """
    if instance.transaction_type != 'expense':
        return
    
    try:
        with db_transaction.atomic():
            budget = Budget.objects.select_for_update().get(
                user=instance.user,
                category=instance.category
            )
            
            # Subtract the transaction amount from budget
            budget.amount_spent = max(
                budget.amount_spent - instance.amount,
                Decimal('0')
            )
            budget.save()
    
    except Budget.DoesNotExist:
        # Budget doesn't exist for this category, skip
        pass
    except Exception as e:
        print(f"Error removing transaction from budget: {str(e)}")
