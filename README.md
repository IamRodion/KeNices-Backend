# KeNices-Backend

API REST para la gestión de inventario y ventas para una floristería y tienda de regalos.

---

## Tabla de Contenidos

1. [Tecnologías y dependencias](#tecnologías-y-dependencias)
2. [Modelos de datos](#modelos-de-datos)
3. [Serializers](#serializers)
4. [Vistas](#vistas)
5. [Endpoints y ejemplos de uso](#endpoints-y-ejemplos-de-uso)

---

## Tecnologías y dependencias

### Backend

- **Lenguaje:** Python 3.x
- **Framework principal:** Django REST Framework (DRF)
- **Base de datos:** SQLite (por defecto, fácilmente migrable a PostgreSQL/MySQL)

### Dependencias

| Paquete                       | Versión | Uso                                                              |
| ----------------------------- | ------- | ---------------------------------------------------------------- |
| Django                        | 5.2.1   | Framework principal para el backend                              |
| djangorestframework           | 3.16.0  | Extensión para construir APIs RESTful con Django                 |
| djangorestframework_simplejwt | 5.5.0   | Autenticación basada en JWT para APIs                            |
| django-cors-headers           | 4.7.0   | Permite solicitudes CORS desde el frontend                       |
| PyJWT                         | 2.9.0   | Manejo de tokens JWT                                             |
| python-dotenv                 | 1.1.0   | Carga de variables de entorno desde archivos `.env`              |
| asgiref                       | 3.8.1   | Soporte para ASGI (interfaz asíncrona de servidores para Python) |
| sqlparse                      | 0.5.3   | Utilidad para parseo de SQL, usada internamente por Django       |

#### ¿Por qué estas tecnologías?

- **Django** es robusto, seguro y ampliamente usado para aplicaciones empresariales.
- **DRF** facilita la creación de APIs limpias, seguras y escalables.
- **JWT** permite autenticación segura y stateless, ideal para SPAs y aplicaciones móviles.
- **CORS** es esencial para permitir el acceso desde frontends modernos.
- **SQLite** es simple para desarrollo, pero la estructura es compatible con bases de datos más robustas.

---

## Modelos de datos

El sistema gestiona productos, ventas y los ítems de cada venta.

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    provider = models.CharField(max_length=100)
    registration_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.stock}) @ {self.price}"

class Sale(models.Model):
    sale_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    customer_document_number = models.CharField(max_length=20)

    class Meta:
        ordering = ['-sale_date']

    def __str__(self):
        return f"Sale to {self.customer_name} @ {self.calculate_total()}"

    def calculate_total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity}) -> {self.sale.customer_name}"
```

**Razón del diseño:**

- **Product:** Permite gestionar inventario, proveedores y fechas de expiración.
- **Sale:** Registra cada venta, asociando cliente y fecha.
- **SaleItem:** Permite ventas con múltiples productos y cantidades, manteniendo integridad referencial.

---

## Serializers

Los serializers transforman los modelos a formatos JSON y validan la entrada de datos.

```python
from rest_framework import serializers
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
```

**Razón del diseño:**

- Se usan serializers anidados para mostrar detalles de productos en los ítems de venta.
- Se separa el campo `product_id` para facilitar la creación de ítems desde el frontend.

---

## Vistas

Las vistas exponen los modelos como endpoints RESTful usando DRF.

```python
from rest_framework import viewsets, filters
from .models import Product, Sale, SaleItem
from .serializers import ProductSerializer, SaleSerializer, SaleItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['expiry_date']
    ordering = ['expiry_date']

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
```

**Razón del diseño:**

- Se usan `ModelViewSet` para exponer CRUD completo.
- Se permite ordenar productos por fecha de expiración.

---

## Endpoints y ejemplos de uso

### Productos

- **Listar productos**

  - `GET /api/Product/`
  - **Respuesta:**
    ```json
    [
      {
        "id": 1,
        "name": "Oso de peluche",
        "description": "Oso de peluche de 30cm",
        "price": "20500.0",
        "stock": 100,
        "provider": "Osos S.A.",
        "registration_date": "2025-06-01",
        "expiry_date": "2028-07-01"
      }
    ]
    ```

- **Crear producto**
  - `POST /api/Product/`
  - **Solicitud:**
    ```json
    {
      "name": "Chocolates",
      "description": "Chocolates Surtidos",
      "price": "5000.0",
      "stock": 50,
      "provider": "Chocolates Ltd.",
      "expiry_date": "2025-06-15"
    }
    ```
  - **Respuesta:**
    ```json
    {
      "id": 2,
      "name": "Chocolates",
      "description": "Chocolates Surtidos",
      "price": "5000.0",
      "stock": 50,
      "provider": "Chocolates Ltd.",
      "registration_date": "2024-06-02",
      "expiry_date": "2025-06-15"
    }
    ```

---

### Ventas

- **Listar ventas**

  - `GET /api/Sale/`
  - **Respuesta:**
    ```json
    [
      {
        "id": 1,
        "sale_date": "2025-06-02T10:00:00Z",
        "customer_name": "Juan Pérez",
        "customer_document_number": "12345678",
        "items": [
          {
            "product": {
              "id": 1,
              "name": "Oso de peluche",
              "price": "20500.0"
            },
            "quantity": 1
          },
          {
            "product": {
              "id": 2,
              "name": "Chocolates",
              "price": "5000.0"
            },
            "quantity": 2
          }
        ],
        "total": "21500.0"
      }
    ]
    ```

- **Crear venta**
  - `POST /api/Sale/`
  - **Solicitud:**
    ```json
    {
      "customer_name": "Ana Gómez",
      "customer_document_number": "87654321",
      "items": [
        {
          "product_id": 1,
          "quantity": 2
        },
        {
          "product_id": 2,
          "quantity": 1
        }
      ]
    }
    ```
  - **Respuesta:**
    ```json
    {
      "id": 2,
      "sale_date": "2025-06-02T11:00:00Z",
      "customer_name": "Ana Gómez",
      "customer_document_number": "87654321",
      "items": [
        {
          "product": {
            "id": 1,
            "name": "Oso de peluche",
            "price": "20500.0"
          },
          "quantity": 2
        },
        {
          "product": {
            "id": 2,
            "name": "Chocolates",
            "price": "5000.0"
          },
          "quantity": 1
        }
      ],
      "total": "46000.0"
    }
    ```

---
