from django.urls import path
from . import views

app_name = 'budget'

urlpatterns = [
    path('', views.budgets_view, name='budgets'),
    path('create/', views.budget_create, name='create'),
    path('<int:budget_id>/edit/', views.budget_edit, name='edit'),
    path('<int:budget_id>/delete/', views.budget_delete, name='delete'),
]