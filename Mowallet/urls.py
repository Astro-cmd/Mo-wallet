from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('users/', include('users.urls')),
    path('transactions/', include('transactions.urls')),
    path('budgets/', include('budget.urls')),
    path('analytics/', include('analytics.urls')),
    path('mpesa/', include('mpesa.urls')),
    path('admin/logout/', LogoutView.as_view(), name='logout'),
    # main/urls.py
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)