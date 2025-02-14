from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KPIViewSet, AssetViewSet, AttributeViewSet

router = DefaultRouter()
router.register(r'KPIs', KPIViewSet)
router.register(r'Assets', AssetViewSet)
router.register(r'Linker', AttributeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

