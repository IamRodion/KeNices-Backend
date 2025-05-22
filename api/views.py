from rest_framework import viewsets, generics
# from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Sale, SaleItem
from .serializers import ProductSerializer, SaleSerializer, SaleItemSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer