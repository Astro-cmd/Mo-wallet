from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('transactions/', include('transactions.urls')),
    path('goals/', include('goals.urls')),
    path('budget/', include('budget.urls')),
    path('analytics/', include('analytics.urls')),
    path('mpesa/', include('mpesa.urls')),
    path('wallet/', include('wallet.urls')),
    path('notifications/', include('notifications.urls')),  # Add this line
    path('admin/logout/', LogoutView.as_view(), name='logout'),
    
    # API endpoints for Next.js frontend
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', include('core.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)