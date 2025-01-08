from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DetailView
from django.shortcuts import redirect, render
from .models import Order, OrderItem, Payment
from cart.models import Cart
from .forms import PaymentForm
from products.models import Product
from django.contrib import messages


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
        return redirect('order_detail', id=order.id)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = request.session.get('cart', {})
        cart_products = []
        total_price = 0

        for product_id, quantity in cart_items.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity
            cart_products.append('product')

        form = PaymentForm()

        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'form': form,
        }
        return render(request, 'orders/checkout.html', context)

    def post(self, request):
        cart_items = request.session.get('cart', {})
        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('checkout')

        form = PaymentForm(request.POST)
        if form.is_valid():
            total_price = sum(
                Product.objects.get(id=int(product_id)).price * quantity
                for product_id, quantity in cart_items.items()
            )

            payment = Payment.objects.create(
                user=request.user,
                amount=total_price,
                status='Completed'
            )

            # create an Order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                payment=payment
            )

            # save order items
            for product_id, quantity in cart_items.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price * quantity
                )

                # Clear the cart
                request.session['cart'] ={}
                messages.success(request, 'Your order has been placed successfully!')
                return redirect('orders')
            else:
                messages.error(request, 'Invalid card details. Please try again!')
                return redirect('checkout')
