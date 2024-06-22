from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__id=kwargs['id']).exists():
            return Response(
                {'error': 'Product can not be deleted because it is associated with an order item.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection__id=kwargs['id']).exists():
            return Response(
                {'error': 'Collection can not be deleted because it is associated with a Product.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)
