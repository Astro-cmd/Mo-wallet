from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('featurses/', views.features_view, name='features'),
    path('help/', views.help_view, name='help'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
]

