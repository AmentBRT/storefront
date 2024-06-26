from django.db import transaction

from rest_framework import serializers

from decimal import Decimal

from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem
from .signals import order_created


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count', 'featured_product']


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField('calculate_tax')

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        validated_data['product_id'] = self.context['product_id']
        return super().create(validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('No Product with the given ID was found.')

        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        with transaction.atomic():
            self.instance, created = CartItem.objects.get_or_create(cart_id=cart_id, product_id=product_id, defaults={'quantity': quantity})

            if not created:
                self.instance.quantity += quantity
                self.instance.save()

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, cart: Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, value):
        if not Cart.objects.filter(id=value).exists():
            raise serializers.ValidationError('No cart with the given ID was found.')

        if not CartItem.objects.filter(cart_id=value).exists():
            raise serializers.ValidationError('The cart is empty')

        return value

    def save(self, **kwargs):
        user_id = self.context["user_id"]
        cart_id = self.validated_data['cart_id']

        with transaction.atomic():
            customer = Customer.objects.only('id').get(user_id=user_id)
            order = Order.objects.create(customer_id=customer.id)

            cart_items = CartItem.objects.select_related('product').only('product', 'quantity').filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity,
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.get(id=cart_id).delete()

        order_created.send_robust(self.__class__, order=order)

        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
