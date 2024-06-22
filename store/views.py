from django.db.models import Count

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer
from .models import Product, Collection, OrderItem, Review, Cart
from .filters import ProductFilter
from .pagination import DefaultPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

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


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}


class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
