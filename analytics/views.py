from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction
from budget.models import Budget
from goals.models import SavingsGoal
from django.db.models import Sum, Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
import json
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
    expense_categories_qs = Transaction.objects.filter(
        user=user,
        transaction_type='expense'
    ).values('category').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg_amount=Avg('amount')
    ).order_by('-total')
    expense_categories = list(expense_categories_qs)

    # Time series data for charts (last 12 months, aligned month by month)
    months_labels = []
    income_data = []
    expense_data = []

    for offset in range(11, -1, -1):
        month = today.month - offset
        year = today.year

        while month <= 0:
            month += 12
            year -= 1

        month_start = today.replace(
            year=year,
            month=month,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        if month == 12:
            next_month_start = month_start.replace(year=year + 1, month=1, day=1)
        else:
            next_month_start = month_start.replace(month=month + 1, day=1)

        month_transactions = Transaction.objects.filter(
            user=user,
            transaction_date__gte=month_start,
            transaction_date__lt=next_month_start,
        )

        month_income = month_transactions.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        month_expenses = month_transactions.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        months_labels.append(f"{calendar.month_abbr[month]} {year}")
        income_data.append(float(month_income))
        expense_data.append(float(month_expenses))

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

    budget_safe_count = 0
    budget_warning_count = 0
    budget_critical_count = 0

    for budget in budget_progress:
        pct = float(budget.percentage_used or 0)
        budget.percentage_used_display = min(100.0, max(0.0, pct))
        if pct > 90:
            budget_critical_count += 1
        elif pct > 75:
            budget_warning_count += 1
        else:
            budget_safe_count += 1

    # Goals progress - use the existing progress property
    savings_goals = SavingsGoal.objects.filter(user=user).order_by('-current_savings')

    goals_urgent_count = sum(1 for goal in savings_goals if not goal.completed and goal.days_left < 30)
    goals_completed_count = SavingsGoal.objects.filter(user=user, completed=True).count()
    goal_avg_progress = round(
        sum(float(goal.progress) for goal in savings_goals) / len(savings_goals),
        1
    ) if savings_goals else 0

    top_expense_category = expense_categories[0] if expense_categories else None
    top_expense_category_name = top_expense_category['category'] if top_expense_category else 'No expenses yet'
    top_expense_category_total = float(top_expense_category['total']) if top_expense_category else 0
    avg_daily_spend = round(sum(daily_data) / len(daily_data), 2) if daily_data else 0

    expense_category_labels = [item['category'] for item in expense_categories]
    expense_category_data = [float(item['total']) for item in expense_categories]

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
        'months_labels_json': json.dumps(months_labels),
        'income_data_json': json.dumps(income_data),
        'expense_data_json': json.dumps(expense_data),
        'daily_labels_json': json.dumps(daily_labels),
        'daily_data_json': json.dumps(daily_data),
        'expense_category_labels_json': json.dumps(expense_category_labels),
        'expense_category_data_json': json.dumps(expense_category_data),
        'budget_progress': budget_progress,
        'savings_goals': savings_goals,
        'budget_safe_count': budget_safe_count,
        'budget_warning_count': budget_warning_count,
        'budget_critical_count': budget_critical_count,
        'goals_urgent_count': goals_urgent_count,
        'goals_completed_count': goals_completed_count,
        'goal_avg_progress': goal_avg_progress,
        'top_expense_category_name': top_expense_category_name,
        'top_expense_category_total': top_expense_category_total,
        'avg_daily_spend': avg_daily_spend,
    }
    
    return render(request, 'analytics.html', context)