from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_backends
from django.http import JsonResponse
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transactions.models import Transaction
from budget.models import Budget
from goals.models import SavingsGoal
from wallet.models import Wallet
from .forms import SignupForm
from .serializers import UserSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    """
    Get details of the currently authenticated user
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            backend = get_backends()[0]
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('core:dashboard')  # Change to your desired redirect
        else:
            # Errors will be displayed in the template
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    
    return render(request, 'signup_vision.html', {'form': form})

def validate_signup_view(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = SignupForm(request.POST)
        if form.is_valid():
            return JsonResponse({'success': True})
        else:
            # Return errors in a flat dict {field: error}
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': {'__all__': 'Invalid request.'}}, status=400)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Clear any old messages
            list(messages.get_messages(request))
            
            # Get the next URL from GET parameters
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            request.session['dashboard_message'] = f"Login successful! Welcome, {user.username}!"
            return redirect('core:home')
        else:
            # Clear any old messages
            list(messages.get_messages(request))
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        # Clear any old messages on GET
        list(messages.get_messages(request))
    return render(request, 'login_vision.html', {'form': form})

def logout_view(request):
    logout(request)
    # Clear any old messages
    list(messages.get_messages(request))
    messages.success(request, "You've been logged out.")
    return redirect('core:home')


@login_required
def profile_view(request):
    user = request.user

    monthly_income = Transaction.objects.filter(
        user=user,
        transaction_type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    net_position = monthly_income - monthly_expenses

    active_goals = SavingsGoal.objects.filter(user=user, completed=False).count()
    budgets_count = Budget.objects.filter(user=user).count()
    recent_transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')[:5]

    wallet = Wallet.objects.filter(user=user).first()
    wallet_balance = wallet.balance if wallet else 0

    context = {
        'profile_user': user,
        'wallet_balance': wallet_balance,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'net_position': net_position,
        'active_goals': active_goals,
        'budgets_count': budgets_count,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'profile.html', context)