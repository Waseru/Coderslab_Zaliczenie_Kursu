from django.contrib import admin

# Register your models here.
from orders.models import Product, ProductPart, Order, OrderData

class OrderInLine(admin.TabularInline):
    model = OrderData
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(ProductPart)
class ProductPartAdmin(admin.ModelAdmin):
    list_display = ['part_number', 'product_name', 'quantity', 'expire_date']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderInLine,
    ]
    exclude = ('product',)

