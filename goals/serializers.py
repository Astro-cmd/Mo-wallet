from rest_framework import serializers
from .models import SavingsGoal, GoalContribution

class GoalContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalContribution
        fields = ['id', 'amount', 'date']

class SavingsGoalSerializer(serializers.ModelSerializer):
    contributions = GoalContributionSerializer(many=True, read_only=True)
    progress = serializers.FloatField(read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    days_left = serializers.IntegerField(read_only=True)
    is_achievable = serializers.BooleanField(read_only=True)

    class Meta:
        model = SavingsGoal
        fields = [
            'id', 'goal_name', 'target_amount', 'current_savings',
            'deadline', 'completed', 'progress', 'remaining_amount',
            'days_left', 'is_achievable', 'contributions'
        ]