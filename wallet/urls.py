from django.urls import path
from . import views

app_name = 'wallet'
urlpatterns = [
    path('', views.wallet_list, name='list'),
    path('create/', views.create_wallet, name='create'),
    path('<int:wallet_id>/edit/', views.edit_wallet, name='edit'),
    path('<int:wallet_id>/delete/', views.delete_wallet, name='delete'),
    path('transfer/', views.transfer_funds, name='transfer'),
]