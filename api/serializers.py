from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, Sale, SaleItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class SaleItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product',
        write_only=True
    )

    class Meta:
        model = SaleItem
        fields = ['product', 'product_id', 'quantity']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = '__all__'
        
    def get_total(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Revisa sí la cantidad indicada está en el inventario
            if product.stock < quantity:
                raise ValidationError(f"Not enough stock for product {product.name}. Available: {product.stock}, Requested: {quantity}")
            
            # Reduce el stock del producto
            product.stock -= quantity
            product.save()
            
            # Registra los objetos vendidos
            SaleItem.objects.create(sale=sale, **item_data)
        
        return sale
