from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'Product', views.ProductViewSet)
router.register(r'Sale', views.SaleViewSet)
router.register(r'SaleItem', views.SaleItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]