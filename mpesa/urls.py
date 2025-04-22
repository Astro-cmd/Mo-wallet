from django.urls import path
from . import views
from .views import lipa_na_mpesa_online, send_mpesa_payment
 
urlpatterns = [
    path('payment-notification/', views.mpesa_payment_notification, name='mpesa_payment_notification'),
    path('initiate-transaction/', views.initiate_mpesa_transaction, name='initiate_mpesa_transaction'),
    path('api/lipa/', lipa_na_mpesa_online, name='lipa_na_mpesa_online'),
    path('send/', send_mpesa_payment, name='mpesa_send'),
]
