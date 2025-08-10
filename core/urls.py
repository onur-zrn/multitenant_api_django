from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SampleViewSet, SampleResultViewSet

router = DefaultRouter()
router.register(r'samples', SampleViewSet)
router.register(r'sample-results', SampleResultViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]