from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from budget.models import Budget
from goals.models import SavingsGoal
from django.db.models import Sum, Avg, Count, F, ExpressionWrapper, DecimalField
from django.db.models.functions import ExtractMonth, ExtractYear, TruncDate
from django.utils import timezone
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import calendar

@login_required
def analytics_view(request):
    user = request.user
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (start_of_month - timedelta(days=1)).replace(day=1)
    
    # Basic financial metrics
    total_income = Transaction.objects.filter(user=user, transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(user=user, transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    net_savings = total_income - total_expenses
    savings_rate = round((net_savings / total_income * 100), 2) if total_income > 0 else 0

    # Monthly comparisons
    current_month_income = Transaction.objects.filter(
        user=user, 
        transaction_type='income',
        transaction_date__gte=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    current_month_expenses = Transaction.objects.filter(
        user=user, 
        transaction_type='expense',
        transaction_date__gte=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    last_month_income = Transaction.objects.filter(
        user=user,
        transaction_type='income',
        transaction_date__gte=last_month_start,
        transaction_date__lt=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    last_month_expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        transaction_date__gte=last_month_start,
        transaction_date__lt=start_of_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate trends
    income_change = ((current_month_income - last_month_income) / last_month_income * 100) if last_month_income > 0 else 0
    expense_change = ((current_month_expenses - last_month_expenses) / last_month_expenses * 100) if last_month_expenses > 0 else 0

    # Spending patterns
    expense_categories = Transaction.objects.filter(
        user=user,
        transaction_type='expense'
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg_amount=Avg('amount')
    ).order_by('-total')

    # Time series data for charts
    last_12_months = today - timedelta(days=365)
    monthly_data = Transaction.objects.filter(
        user=user,
        transaction_date__gte=last_12_months
    ).annotate(
        month=ExtractMonth('transaction_date'),
        year=ExtractYear('transaction_date')
    ).values('month', 'year', 'transaction_type').annotate(
        total=Sum('amount')
    ).order_by('year', 'month')

    # Prepare chart data
    months_labels = []
    income_data = [0] * 12
    expense_data = [0] * 12
    
    for data in monthly_data:
        month_idx = data['month'] - 1
        if data['transaction_type'] == 'income':
            income_data[month_idx] = float(data['total'])
        else:
            expense_data[month_idx] = float(data['total'])
        if len(months_labels) < 12:
            month_name = calendar.month_abbr[data['month']]
            months_labels.append(f"{month_name} {data['year']}")

    # Daily spending patterns
    daily_expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense',
        transaction_date__gte=today - timedelta(days=30)
    ).annotate(
        day_date=TruncDate('transaction_date')
    ).values('day_date').annotate(
        total=Sum('amount')
    ).order_by('day_date')

    daily_labels = []
    daily_data = []
    for expense in daily_expenses:
        daily_labels.append(expense['day_date'].strftime('%d %b'))
        daily_data.append(float(expense['total']))

    # Budget analysis
    budget_progress = Budget.objects.filter(user=user).order_by('-amount_spent')

    # Goals progress - use the existing progress property
    savings_goals = SavingsGoal.objects.filter(user=user).order_by('-current_savings')

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_savings': net_savings,
        'savings_rate': savings_rate,
        'current_month_income': current_month_income,
        'current_month_expenses': current_month_expenses,
        'income_change': round(income_change, 1),
        'expense_change': round(expense_change, 1),
        'expense_categories': list(expense_categories),
        'months_labels': months_labels,
        'income_data': income_data,
        'expense_data': expense_data,
        'daily_labels': daily_labels,
        'daily_data': daily_data,
        'budget_progress': budget_progress,
        'savings_goals': savings_goals,
    }
    
    return render(request, 'analytics.html', context)