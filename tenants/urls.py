from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CenterViewSet, DomainViewSet

router = DefaultRouter()
router.register(r'centers', CenterViewSet)
router.register(r'domains', DomainViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]