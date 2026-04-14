# core/views_vision.py
"""
Vision UI Dashboard Views
Modern dashboard views for Mo-wallet using Vision UI design system
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count
from django.http import JsonResponse
from transactions.models import Transaction
from goals.models import SavingsGoal
from budget.models import Budget
from core.categories import TRANSACTION_CATEGORIES
from datetime import timedelta, datetime
from decimal import Decimal
import json


@login_required
def dashboard_vision(request):
    """
    Vision UI Dashboard - Modern financial overview
    """
    user = request.user
    now = timezone.now()
    today = now.date()
    
    # Time periods
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_of_week = now - timedelta(days=now.weekday())
    
    # ===== TODAY'S METRICS =====
    today_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_today
    )
    
    today_income = today_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    today_expenses = today_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    # ===== MONTHLY METRICS =====
    month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_month
    )
    
    total_income = month_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    total_expenses = month_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    monthly_savings = total_income - total_expenses
    savings_rate = (monthly_savings / total_income * 100) if total_income > 0 else 0
    
    # ===== TRENDS (vs last month) =====
    last_month_start = (now.replace(day=1) - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_end = (now.replace(day=1) - timedelta(seconds=1))
    
    last_month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=last_month_start,
        transaction_date__lt=last_month_end
    )
    
    last_month_income = last_month_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('1')
    
    income_trend = ((total_income - last_month_income) / last_month_income * 100) if last_month_income > 0 else 0
    expense_trend = 0  # Calculate if needed
    
    # ===== PERCENTAGES =====
    total_money = total_income + total_expenses
    income_percentage = (total_income / total_money * 100) if total_money > 0 else 0
    expense_percentage = (total_expenses / total_money * 100) if total_money > 0 else 0
    
    # ===== BUDGETS =====
    budgets = Budget.objects.filter(user=user)
    for budget in budgets:
        spent = month_transactions.filter(
            category=budget.category,
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        budget.amount_spent = spent
        budget.percentage_used = min(100, (spent / budget.limit * 100) if budget.limit > 0 else 0)
    
    # ===== GOALS =====
    active_goals = SavingsGoal.objects.filter(user=user, completed=False).order_by('-created_at')[:3]
    active_goals_count = SavingsGoal.objects.filter(user=user, completed=False).count()
    
    # ===== RECENT TRANSACTIONS =====
    recent_transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')[:5]
    
    # ===== EXPENSE BREAKDOWN =====
    expense_breakdown = month_transactions.filter(
        transaction_type='expense'
    ).values('category').annotate(total=Sum('amount')).order_by('-total')
    
    expense_labels = [
        dict(TRANSACTION_CATEGORIES).get(item['category'], item['category'])
        for item in expense_breakdown
    ]
    expense_data = [float(item['total']) for item in expense_breakdown]
    
    # ===== SPENDING DATA =====
    last_6_months_income = []
    last_6_months_expenses = []
    
    for i in range(6, 0, -1):
        month_start = (now - timedelta(days=30*i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = (month_start + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        month_data = Transaction.objects.filter(
            user=user,
            transaction_date__gte=month_start,
            transaction_date__lt=month_end
        )
        
        month_inc = month_data.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        month_exp = month_data.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        last_6_months_income.append(float(month_inc))
        last_6_months_expenses.append(float(month_exp))
    
    # ===== UNREAD NOTIFICATIONS =====
    unread_notifications = 0  # Implement based on your notifications model
    
    context = {
        'user': user,
        'today_income': today_income,
        'today_expenses': today_expenses,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'monthly_savings': monthly_savings,
        'savings_rate': savings_rate,
        'income_trend': income_trend,
        'expense_trend': expense_trend,
        'income_percentage': income_percentage,
        'expense_percentage': expense_percentage,
        'budgets': budgets,
        'active_goals': active_goals,
        'active_goals_count': active_goals_count,
        'recent_transactions': recent_transactions,
        'expense_labels': json.dumps(expense_labels),
        'expense_data': json.dumps(expense_data),
        'unread_notifications': unread_notifications,
        'current_month_name': now.strftime('%B %Y'),
    }
    
    return render(request, 'dashboard_vision.html', context)


@login_required
def budgets_vision(request):
    """
    Vision UI Budgets - Modern budget management
    """
    user = request.user
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get transactions for this month
    month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_month
    )
    
    # Get all budgets
    budgets = Budget.objects.filter(user=user)
    
    total_budget = Decimal('0')
    total_spent = Decimal('0')
    all_budgets_data = []
    
    for budget in budgets:
        spent = month_transactions.filter(
            category=budget.category,
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        total_budget += budget.limit
        total_spent += spent
        
        budget_data = {
            'id': budget.id,
            'category': budget.category,
            'category_display': budget.get_category_display(),
            'limit': budget.limit,
            'amount_spent': spent,
            'remaining': budget.limit - spent,
            'percentage_used': min(100, (spent / budget.limit * 100) if budget.limit > 0 else 0),
        }
        all_budgets_data.append(budget_data)
    
    remaining_budget = total_budget - total_spent
    spent_percentage = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    context = {
        'budgets': all_budgets_data,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'spent_percentage': spent_percentage,
    }
    
    return render(request, 'budgets_vision.html', context)


@login_required
def analytics_vision(request):
    """
    Vision UI Analytics - Modern financial analysis
    """
    user = request.user
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get monthly data
    month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_month
    )
    
    # Calculate metrics
    total_income = month_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    total_expenses = month_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
    
    # Expense breakdown by category
    expense_breakdown = month_transactions.filter(
        transaction_type='expense'
    ).values('category').annotate(total=Sum('amount')).order_by('-total')
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'expense_breakdown': expense_breakdown,
    }
    
    return render(request, 'analytics_vision.html', context)


@login_required
def transactions_vision(request):
    """
    Vision UI Transactions - Modern transaction management
    """
    user = request.user
    
    # Filter transactions
    transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')
    
    # Apply filters if provided
    transaction_type = request.GET.get('type')
    category = request.GET.get('category')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    if category:
        transactions = transactions.filter(category=category)
    
    if date_from:
        transactions = transactions.filter(transaction_date__gte=date_from)
    
    if date_to:
        transactions = transactions.filter(transaction_date__lte=date_to)
    
    # Pagination
    page = request.GET.get('page', 1)
    per_page = 20
    start = (int(page) - 1) * per_page
    end = start + per_page
    
    total_pages = (transactions.count() + per_page - 1) // per_page
    transactions_page = transactions[start:end]
    
    context = {
        'transactions': transactions_page,
        'page': int(page),
        'total_pages': total_pages,
        'categories': TRANSACTION_CATEGORIES,
    }
    
    return render(request, 'transactions_vision.html', context)


@login_required
def api_dashboard_stats(request):
    """
    API endpoint for dashboard statistics
    Returns real-time stats for dashboard
    """
    user = request.user
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_month
    )
    
    total_income = month_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = month_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    return JsonResponse({
        'income': float(total_income),
        'expenses': float(total_expenses),
        'savings': float(total_income - total_expenses),
        'savings_rate': (((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0),
    })
