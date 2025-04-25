from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'users'

urlpatterns = [
    
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('validate-signup/', views.validate_signup_view, name='validate-signup'),
    
    # API endpoints
    path('api/me/', views.user_details, name='user-details'),
]



