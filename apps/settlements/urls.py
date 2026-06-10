from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SettlementViewSet

router = DefaultRouter()
router.register('', SettlementViewSet, basename='settlement')

urlpatterns = [path('', include(router.urls))]
