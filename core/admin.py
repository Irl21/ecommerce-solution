from django.contrib import admin
from cart.models import Product, Address, Payment, Order, OrderItem, ColorVariation, SizeVariation


admin.site.register(Product)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(ColorVariation)
admin.site.register(SizeVariation)
# Register your models here.
