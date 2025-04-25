from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from core.categories import TRANSACTION_CATEGORIES
from .forms import BudgetForm
from .models import Budget
from transactions.models import Transaction

@login_required
def budgets_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget created successfully.")
            return redirect('budget:budgets')
    else:
        form = BudgetForm()

    # Get all budgets for the user
    budgets = Budget.objects.filter(user=request.user)
    
    # Apply search filter if provided
    search_query = request.GET.get('search', '')
    if search_query:
        budgets = budgets.filter(
            Q(category__icontains=search_query) | 
            Q(limit__icontains=search_query)
        )
    
    # Apply category filter if provided
    category_filter = request.GET.get('category', '')
    if category_filter:
        budgets = budgets.filter(category=category_filter)
    
    # Apply date filters if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date:
        budgets = budgets.filter(created_at__gte=start_date)
    if end_date:
        budgets = budgets.filter(created_at__lte=end_date)
    
    # Calculate totals
    total_budget = budgets.aggregate(total=Sum('limit'))['total'] or 0
    total_spent = budgets.aggregate(total=Sum('amount_spent'))['total'] or 0
    total_remaining = total_budget - total_spent

    # Setup pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(budgets, 12)  # Show 12 budgets per page
    try:
        budgets = paginator.page(page)
    except PageNotAnInteger:
        budgets = paginator.page(1)
    except EmptyPage:
        budgets = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'budgets': budgets,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'search_query': search_query,
        'category_filter': category_filter,
        'start_date': start_date,
        'end_date': end_date,
        'categories': TRANSACTION_CATEGORIES
    }
    return render(request, 'budget_list.html', context)

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget created successfully.")
            return redirect('budget:budgets')
    else:
        form = BudgetForm()
    
    return render(request, 'budget_create.html', {'form': form})

@login_required
def budget_edit(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    
    # Get related transactions for the current month
    current_month = timezone.now().month
    current_year = timezone.now().year
    transactions = Transaction.objects.filter(
        user=request.user,
        category=budget.category,
        transaction_date__month=current_month,
        transaction_date__year=current_year
    ).order_by('-transaction_date')
    
    total_transactions = transactions.aggregate(total=Sum('amount'))['total'] or 0

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully.")
            return redirect('budget:budgets')
    else:
        form = BudgetForm(instance=budget)

    context = {
        'form': form,
        'budget': budget,
        'transactions': transactions,
        'total_transactions': total_transactions
    }
    return render(request, 'budget_edit.html', context)

@login_required
def budget_delete(request, budget_id):
    if request.method == 'POST':
        budget = get_object_or_404(Budget, id=budget_id, user=request.user)
        budget.delete()
        messages.success(request, "Budget deleted successfully.")
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('budget:budgets')
    return JsonResponse({'status': 'error'}, status=405)

