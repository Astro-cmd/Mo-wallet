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
from core.views_vision import dashboard_vision

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
    """Dashboard view (Vision UI)."""
    return dashboard_vision(request)