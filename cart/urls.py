from django.urls import path
from .views import CartView, AddToCartView, RemoveFromCartView, IncreaseQuantityView, DecreaseCartItemView

urlpatterns = [
    path('', CartView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('increase/<int:item_id>/', IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease/<int:item_id>/', DecreaseCartItemView.as_view(), name='decrease-cart-item'),
]