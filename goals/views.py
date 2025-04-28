from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from decimal import Decimal
from .models import SavingsGoal, GoalContribution
from .forms import GoalForm
from .serializers import SavingsGoalSerializer, GoalContributionSerializer

@login_required
def goals_list(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    total_target = sum(goal.target_amount for goal in goals)
    total_saved = sum(goal.current_savings for goal in goals)
    overall_progress = (total_saved / total_target * 100) if total_target > 0 else 0
    
    context = {
        'goals': goals,
        'form': GoalForm(),
        'total_goals': goals.count(),
        'total_target': total_target,
        'total_saved': total_saved,
        'overall_progress': round(overall_progress, 1)
    }
    return render(request, 'goals.html', context)

@login_required
@transaction.atomic
@require_POST
def add_contribution(request):
    goal_id = request.POST.get('goal_id')
    amount = request.POST.get('amount')
    
    if not goal_id or not amount:
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
    
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
    
    try:
        amount = Decimal(amount)
        
        # Validate wallet balance
        if request.user.wallet.balance < amount:
            raise ValidationError("Insufficient funds in wallet")
        
        # Create contribution with transaction
        contribution = goal.add_contribution(amount)
        messages.success(request, f'Successfully added contribution of KES {amount:,.2f} to {goal.goal_name}')
        return JsonResponse({
            'status': 'success',
            'current_savings': float(goal.current_savings),
            'progress': float(goal.progress),
            'completed': goal.completed,
            'contribution': {
                'id': contribution.id,
                'amount': float(contribution.amount),
                'date': contribution.date.isoformat()
            }
        })
    except (ValidationError, ValueError, TypeError) as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_POST
def create_goal(request):
    form = GoalForm(request.POST)
    if form.is_valid():
        goal = form.save(commit=False)
        goal.user = request.user
        try:
            goal.save()
            messages.success(request, f'Goal "{goal.goal_name}" created successfully!')
            return redirect('goals:list')
        except ValidationError as e:
            messages.error(request, str(e))
    else:
        messages.error(request, 'Please correct the errors below.')
    return redirect('goals:list')

@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Goal "{goal.goal_name}" updated successfully!')
                return redirect('goals:list')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goal_edit_form.html', {'form': form, 'goal': goal})

@login_required
@require_POST
def delete_goal(request, goal_id):
    goal = get_object_or_404(SavingsGoal, id=goal_id, user=request.user)
    try:
        if goal.can_delete():
            goal_name = goal.goal_name
            goal.delete()
            messages.success(request, f'Goal "{goal_name}" deleted successfully!')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Cannot delete a goal that has contributions or is completed.'
            })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def contributions(self, request, pk=None):
        goal = self.get_object()
        contributions = goal.contributions.all()
        serializer = GoalContributionSerializer(contributions, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def add_contribution(self, request, pk=None):
        goal = self.get_object()
        amount = Decimal(request.data.get('amount', 0))
        
        try:
            # Validate wallet balance
            if request.user.wallet.balance < amount:
                raise ValidationError("Insufficient funds in wallet")
                
            contribution = goal.add_contribution(amount)
            serializer = GoalContributionSerializer(contribution)
            return Response({
                'status': 'success',
                'contribution': serializer.data,
                'current_savings': float(goal.current_savings),
                'progress': float(goal.progress),
                'completed': goal.completed
            })
        except ValidationError as e:
            return Response({'status': 'error', 'message': str(e)}, status=400)

