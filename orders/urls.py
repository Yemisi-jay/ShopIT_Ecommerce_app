from django.urls import path
from .views import PlaceOrder, OrderDetailView, OrdersView, CheckoutView

urlpatterns = [
    path('place/', PlaceOrder.as_view(), name='place_order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]