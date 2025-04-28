from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction, Goal, Budget

@login_required
def dashboard(request):
    user = request.user

    # Fetch user-specific data
    transactions = Transaction.objects.filter(user=user).order_by('-date')[:5]
    goals = Goal.objects.filter(user=user)
    budgets = Budget.objects.filter(user=user)

    # Calculate financial stats
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0

    # Prepare data for charts
    income_by_month = transactions.filter(type='income').values('date__month').annotate(total=Sum('amount'))
    expense_by_month = transactions.filter(type='expense').values('date__month').annotate(total=Sum('amount'))

    context = {
        'user': user,
        'transactions': transactions,
        'goals': goals,
        'budgets': budgets,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_savings': net_savings,
        'savings_rate': savings_rate,
        'income_by_month': income_by_month,
        'expense_by_month': expense_by_month,
    }
    return render(request, 'dashboard.html', context)
