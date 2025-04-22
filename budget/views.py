from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BudgetForm
from .models import Budget

def budgets_view(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget saved successfully.")
            return redirect('budget:budgets')
    else:
        form = BudgetForm()

    budgets = Budget.objects.all()
    return render(request, 'budgets.html', {
        'form': form,
        'budgets': budgets
    })
