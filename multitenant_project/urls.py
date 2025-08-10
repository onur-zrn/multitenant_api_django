# multitenant_project/urls.py (Main URLs - for tenant schemas)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Tenant-specific URLs
]