from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    if product.orderitems.count() > 0:
        return Response(
            {'error': 'Product can not be deleted because it is associated with an order item.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.select_related('featured_product').annotate(products_count=Count('product')).all()
        serializer = CollectionSerializer(queryset, many=True)

        return Response(serializer.data)

    serializer = CollectionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, id):
    collection = get_object_or_404(
        Collection.objects.select_related('featured_product').annotate(products_count=Count('product')),
        id=id,
    )

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)

        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    if collection.products.count() > 0:
        return Response(
            {'error': 'Collection can not be deleted because it is associated with a Product.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )
    collection.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
