from rest_framework import serializers

from decimal import Decimal

from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField('calculate_tax')

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)
