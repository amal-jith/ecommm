from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billing_name', 'billing_email', 'order_date']
    list_filter = ['order_date']
    search_fields = ['billing_name', 'billing_email']
    readonly_fields = ['id', 'order_date']
    ordering = ['-order_date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity']
    list_filter = ['order']
    search_fields = ['order__billing_name', 'product__name']
    readonly_fields = ['id']
