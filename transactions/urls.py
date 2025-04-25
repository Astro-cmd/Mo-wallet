from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('', views.transactions_view, name='transactions'),
    path('<int:transaction_id>/edit/', views.transaction_edit, name='edit'),
    path('<int:transaction_id>/delete/', views.transaction_delete, name='delete'),
]