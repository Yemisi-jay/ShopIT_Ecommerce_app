from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product','quantity', 'total_price', 'created_at')
    list_filter = ('user', 'created_at')


admin.site.register(Cart)

