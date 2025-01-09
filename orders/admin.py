from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter =('status', 'created_at')
    search_fields = ('id', 'user__username')
    ordering = ('-created_at',)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'total_price')
    search_fields = ('order__id', 'product', 'quantity')


admin.site.register(Order, OrderAdmin)
