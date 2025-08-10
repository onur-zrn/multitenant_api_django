# multitenant_project/urls_public.py (Public schema URLs)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tenants.urls')),  # Center management
    path('', include('users.urls')),    # User management
]