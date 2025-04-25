from django.db.models.signals import post_save, pre_delete
from django.db import models
from django.dispatch import receiver
from .models import SavingsGoal, GoalContribution
from django.contrib import messages

@receiver(post_save, sender=GoalContribution)
def update_goal_on_contribution(sender, instance, created, **kwargs):
    """Update goal progress when a contribution is made."""
    if created:
        goal = instance.goal
        goal.current_savings = goal.contributions.aggregate(total=models.Sum('amount'))['total'] or 0
        if goal.current_savings >= goal.target_amount:
            goal.completed = True
        goal.save()

@receiver(pre_delete, sender=GoalContribution)
def update_goal_on_contribution_delete(sender, instance, **kwargs):
    """Update goal when a contribution is deleted."""
    goal = instance.goal
    goal.current_savings -= instance.amount
    goal.completed = goal.current_savings >= goal.target_amount
    goal.save()