from django.urls import path
from .views import PlaceOrder, OrderDetailView


urlpatterns = [
    path('place/', PlaceOrder.as_view(), name='place_order'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]