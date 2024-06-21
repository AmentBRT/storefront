from rest_framework import serializers

from decimal import Decimal

from .models import Product, Collection


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField('calculate_tax')
    collection = serializers.HyperlinkedRelatedField(
        'collection-detail',
        queryset=Collection.objects.all(),
        lookup_field='id',
    )

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)
