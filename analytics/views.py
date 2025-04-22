from django.shortcuts import render
from transactions.models import Transaction
from budget.models import Budget
from django.db.models import Sum

def analytics_view(request):
    # Calculate total income and expenses
    total_income = Transaction.objects.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate budget utilization
    budgets = Budget.objects.all()
    budget_data = [
        {
            'category': budget.get_category_display(),
            'limit': budget.monthly_limit,
            'spent': budget.amount_spent,
            'remaining': budget.remaining
        }
        for budget in budgets
    ]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'budget_data': budget_data
    }
    return render(request, 'analytics.html', context)
