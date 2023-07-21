from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Order, OrderItem, Product, ShippingAddress, Tag

admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
