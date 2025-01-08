from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_seller', 'is_buyer', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(CustomUser)




