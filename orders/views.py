from django.views.generic import View, DetailView
from django.shortcuts import redirect
from .models import Order, OrderItem
from cart.models import Cart


class PlaceOrder(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(user=request.user)
        total_price = 0

        for item in cart.items.all():
            product = item.product
            if product.stock < item.quantity:
                return "Out of stock"

            product.stock -= item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price * item.quantity
            )
            total_price += item.product.price * item.quantity

        order.total_price = total_price
        order.save()
        cart.items.all().delete()
        return redirect('order_detail', pk=order.id)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
