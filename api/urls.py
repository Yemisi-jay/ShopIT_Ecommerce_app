from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, OrderViewSet, CartViewSet, UserViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('profiles', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('cart', CartViewSet)
router.register('users', UserViewSet)


urlpatterns = router.urls
