from rest_framework import serializers

from cart.models import CartItem, Cart
from orders.models import OrderItem, Order
from products.models import Product, Category
from accounts.models import Profile
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

    class Meta:
        model = Profile
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

    def create(self, validated_data):
        # Extract items data
        items_data = validated_data.pop('items')

        # Create the Cart instance
        cart = Cart.objects.create(**validated_data)

        # Get the user from the cart data
        user = cart.user

        # Create CartItem instances
        for item_data in items_data:
            # Check for product
            product_id = item_data.get('product', {}).get('id')
            if not product_id:
                product = Product.objects.first()  # Get the first Product if no ID is provided
                if not product:
                    raise serializers.ValidationError("No products available to assign to cart items.")
            else:
                product = Product.objects.get(id=product_id)

            # Create the CartItem and associate it with the user and cart
            CartItem.objects.create(
                cart=cart,
                user=user,  # Ensure the user is associated with the CartItem
                product=product,
                quantity=item_data['quantity']
            )

        return cart
class OrderItemSerializer(serializers.ModelSerializer):
    product = CartItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'payment']  # Removed 'items' from the fields

    def create(self, validated_data):
        user = validated_data['user']
        payment = validated_data.get('payment')
        total_price = validated_data.get('total_price')

        # Fetch the latest cart for the user
        cart = Cart.objects.filter(user=user).order_by('-created_at').first()  # Get the latest cart

        if not cart:
            raise serializers.ValidationError("No cart found for the user.")

        # Create the order instance
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            payment=payment
        )

        # Loop through cart items and create corresponding order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price * cart_item.quantity  # Calculate price if needed
            )

        # Clear the cart (optional)
        cart.items.all().delete()

        return order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'is_seller', 'is_buyer', "password"]
