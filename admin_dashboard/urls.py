from django.urls import path
from .views import (
    AnalyticsDashboardView,
    ProductManagementView,
    EditProductView,
    DeleteProductView,
)

app_name = 'admin_dashboard'

urlpatterns = [
    path('analytics/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
    path('manage-products/', ProductManagementView.as_view(), name='manage_products'),
    path('edit-product/<int:product_id>/', EditProductView.as_view(), name='edit_product'),
    path('delete-product/<int:product_id>/', DeleteProductView.as_view(), name='delete_product'),
]
