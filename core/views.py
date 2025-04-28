from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from transactions.models import Transaction
from goals.models import SavingsGoal
from budget.models import Budget
from core.categories import TRANSACTION_CATEGORIES
from datetime import timedelta

def home(request):
    """Home page view"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'home.html')

def features_view(request):
    """Features page view"""
    return render(request, 'features.html')

def help_view(request):
    """Help page view"""
    return render(request, 'help.html')

def terms_view(request):
    """Terms of service view"""
    return render(request, 'terms.html')

def privacy_view(request):
    """Privacy policy view"""
    return render(request, 'privacy.html')

def home_data(request):
    """API endpoint for home page data"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    # Add implementation here
    return JsonResponse({})

@login_required
def dashboard_view(request):
    """Dashboard view"""
    user = request.user
    today = timezone.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Get current month's transactions
    current_month_transactions = Transaction.objects.filter(
        user=user,
        transaction_date__gte=start_of_month
    )
    
    # Calculate total balance from all wallets
    total_balance = user.wallet.balance if hasattr(user, 'wallet') else 0
    
    # Calculate financial metrics
    current_month_income = current_month_transactions.filter(
        transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    current_month_expenses = current_month_transactions.filter(
        transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate percentages and rates
    total_money = current_month_income + current_month_expenses
    income_percentage = (current_month_income / total_money * 100) if total_money > 0 else 0
    expense_percentage = (current_month_expenses / total_money * 100) if total_money > 0 else 0
    savings_rate = ((current_month_income - current_month_expenses) / current_month_income * 100) if current_month_income > 0 else 0
    
    # Get budgets with progress
    budgets = Budget.objects.filter(user=user)
    for budget in budgets:
        spent = current_month_transactions.filter(
            category=budget.category,
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        budget.spent = spent
        budget.percentage = min(100, (spent / budget.limit * 100) if budget.limit > 0 else 0)
    
    # Get active goals
    goals = SavingsGoal.objects.filter(user=user, completed=False)
    
    # Get expense breakdown by category
    expense_by_category = current_month_transactions.filter(
        transaction_type='expense'
    ).values('category').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Prepare chart data
    category_labels = [dict(TRANSACTION_CATEGORIES)[exp['category']] for exp in expense_by_category]
    category_amounts = [float(exp['total']) for exp in expense_by_category]

    # Get recent transactions with status
    recent_transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')[:5]
    for transaction in recent_transactions:
        if transaction.transaction_type == 'income':
            transaction.status = 'Completed'
            transaction.status_color = 'success'
        else:
            if transaction.amount > budget.monthly_limit:
                transaction.status = 'Over Budget'
                transaction.status_color = 'danger'
            else:
                transaction.status = 'Within Budget'
                transaction.status_color = 'success'

    context = {
        'total_balance': total_balance,
        'monthly_income': current_month_income,
        'monthly_expenses': current_month_expenses,
        'savings_rate': savings_rate,
        'income_percentage': income_percentage,
        'expense_percentage': expense_percentage,
        'recent_transactions': recent_transactions,
        'budgets': budgets,
        'goals': goals,
        'categories': TRANSACTION_CATEGORIES,
        'expense_labels': category_labels,
        'expense_data': category_amounts,
    }
    
    return render(request, 'dashboard.html', context)