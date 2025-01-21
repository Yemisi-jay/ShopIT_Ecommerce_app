from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
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


class OrdersView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'orders/order_list.html', {'orders': orders})


class CheckoutView(LoginRequiredMixin, View):
    def is_profile_complete(self, user):
        """Check if the user's profile is complete."""
        profile = getattr(user, 'profile', None)
        required_fields = ['address', 'phone_number']
        if not profile:
            return False
        for field in required_fields:
            if not getattr(profile, field, None):
                return False
        return True

    def get(self, request):
        if not self.is_profile_complete(request.user):
            messages.error(request, 'Please complete your profile before checking out.')
            return redirect('profile_edit')

            # Get or create user-based cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('cart_detail')

        cart_items = cart.items.all()
        total_price = cart.items.aggregate(
            total_price=Sum(F('quantity') * F('product__price'))
        )['total_price'] or 0.0

        form = PaymentForm()
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
            'form': form,
        }
        return render(request, 'orders/checkout.html', context)

    def post(self, request):
        if not self.is_profile_complete(request.user):
            messages.error(request, 'Please complete your profile before checking out.')
            return redirect('profile_edit')

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.error(request, "Your cart is empty!")
            return redirect('cart_detail')

        # Handle payment form
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Mimic payment processing
            total_price = cart.items.aggregate(
                total_price=Sum(F('quantity') * F('product__price'))
            )['total_price'] or 0.0

            payment = Payment.objects.create(
                user=request.user,
                amount=total_price,
                status='Completed'
            )

            # Create an order
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                payment=payment
            )

            # Create order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price * item.quantity
                )

            # Clear the cart
            cart.items.all().delete()
            messages.success(request, "Your order has been placed successfully!")
            return redirect('orders')  # Redirect to the orders page

        else:
            messages.error(request, "Invalid payment details. Please try again.")
            return redirect('checkout')
