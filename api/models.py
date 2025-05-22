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
        return self.name

class Sale(models.Model):
    sale_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100)
    customer_document_number = models.CharField(max_length=20)

    def __str__(self):
        return f"Sale to {self.customer_name}"

    def calculate_total(self):
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"