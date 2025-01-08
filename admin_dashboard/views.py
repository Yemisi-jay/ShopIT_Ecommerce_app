from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from admin_dashboard.forms import ProductForm
from products.models import Product
from orders.models import Order
from accounts.models import CustomUser
from django.db.models import Sum


class AnalyticsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "admin_dashboard/analytics.html"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """Redirect non-admin users to the login page or 403 page."""
        from django.http import HttpResponseForbidden
        if self.request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to view this page.")
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        """Add analytics data to the context."""
        context = super().get_context_data(**kwargs)
        context['total_users'] = CustomUser.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_orders'] = Order.objects.count()
        context['total_revenue'] = Order.objects.aggregate(
            revenue=Sum('total_price')
        )['revenue'] or 0
        return context


class ProductManagementView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "admin_dashboard/manage_products.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        products = Product.objects.all()
        form = ProductForm()
        return render(request, self.template_name, {'products': products, 'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard:manage_products")
        products = Product.objects.all()
        return render(request, self.template_name, {'products': products, 'form': form})


class EditProductView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(instance=product)
        return render(request, "admin_dashboard/edit_product.html", {'product': product, 'form': form})

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard:manage_products")
        return render(request, "admin_dashboard/edit_product.html", {'product': product, 'form': form})


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, product_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return redirect("admin_dashboard:manage_products")