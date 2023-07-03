from django.contrib import admin

from .models import Category, Order, OrderItem, Product, ShippingAddress, Tag

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
# admin.site.register(Customer)
