from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from .filters import ProductFilter


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        product_filter = ProductFilter(self.request.GET, queryset=queryset)
        print("Filtered Queryset:", product_filter.qs)
        return product_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object.category
        recommended_products = Product.objects.filter(category=category).exclude(id=self.object.id)[:4]
        context['recommended_products'] = recommended_products
        return context
