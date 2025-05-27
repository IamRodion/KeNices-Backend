from django.contrib import admin
from .models import Product, Sale, SaleItem


# Register your models here.

admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SaleItem)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     """
#     Datos del modelo Product:
#     name
#     description
#     price
#     stock
#     provider
#     registration_date
#     expiry_date
#     """
#     list_display = ('id', 'name', 'price', 'stock', 'expiry_date')
#     list_display_links = ('id',)
#     list_filter = ('stock', 'name', 'provider', 'expiry_date')
#     list_per_page = 10
#     ordering = ('stock', 'expiry_date', 'name')
#     search_fields = ('name', 'description', 'provider')



# @admin.register(Sale)
# class SaleAdmin(admin.ModelAdmin):
#     pass

# @admin.register(SaleItem)
# class SaleItemAdmin(admin.ModelAdmin):
#     pass