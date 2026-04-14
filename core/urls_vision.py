# core/urls_vision.py
"""
Vision UI URLs
URL configuration for Vision UI dashboard views
"""

from django.urls import path
from core.views_vision import (
    dashboard_vision,
    budgets_vision,
    analytics_vision,
    transactions_vision,
    api_dashboard_stats,
)

app_name = 'core_vision'

urlpatterns = [
    # Vision UI Dashboard
    path('dashboard/vision/', dashboard_vision, name='dashboard_vision'),
    
    # Vision UI Pages
    path('budgets/vision/', budgets_vision, name='budgets_vision'),
    path('analytics/vision/', analytics_vision, name='analytics_vision'),
    path('transactions/vision/', transactions_vision, name='transactions_vision'),
    
    # API Endpoints
    path('api/dashboard-stats/', api_dashboard_stats, name='api_dashboard_stats'),
]
