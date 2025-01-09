from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from django.db.models import F, Sum


class CartView(ListView):
    # model = CartItem
    # template_name = 'cart/cart_detail.html'
    # context_object_name = 'cart_items'
    #
    # def get_queryset(self):
    #     cart, created = Cart.objects.get_or_create(user=self.request.user)
    #     return cart.items.all()

    def get(self, request):
        if request.user.is_authenticated:
            # Logged-in user: Use their cart
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # Guest user: Use session-based cart
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = Cart.objects.filter(id=cart_id).first()
            else:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id

        # Get cart items to display
        cart_items = cart.items.all() if cart else []

        total_cost = cart.items.aggregate(
            total_price=Sum(F('quantity') * F('product__price'))
        )['total_price'] or 0.0
        context = {'cart_items': cart_items, 'cart': cart, 'total_cost': total_cost}
        return render(request, 'cart/cart_detail.html', context)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1, 'user': request.user}
        )
        if not created:
            cart_item.quantity += 1
            # cart_item.user = request.user
            cart_item.save()

        if created:
            messages.success(request, 'Item has been added to your cart')
        else:
            messages.success(request, 'Item quantity updated in your cart')
        return redirect('cart_detail')


class RemoveFromCartView(RedirectView):
    pattern_name = 'cart_detail'

    def get(self, *args, **kwargs):
        cart_item = get_object_or_404(CartItem, id=self.kwargs['item_id'])
        cart_item.delete()
        return super().get_redirect_url(*args, **kwargs)


class IncreaseQuantityView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, user=self.request.user)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Item quantity updated in your cart')
        return redirect('cart_detail')


class DecreaseCartItemView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart_detail')

