from rest_framework import serializers

from decimal import Decimal

from .models import Product, Collection, Review, Cart


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


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id']
