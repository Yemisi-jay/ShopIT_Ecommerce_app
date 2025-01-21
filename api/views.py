from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from cart.models import Cart
from orders.models import Order
from products.models import Product, Category
from .serializer import ProductSerializer, CategorySerializer, ProfileSerializer, CartSerializer, OrderSerializer, UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProfileSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
