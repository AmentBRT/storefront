from django.shortcuts import render
from django.db.models  import Q, F
from store.models import Product, OrderItem, Order


def say_hello(request):
    queryset = Product.objects.filter(unit_price__range=(20, 30))
    queryset = Product.objects.filter(Q(unit_price=20) | Q(inventory=20))
    queryset = Product.objects.filter(inventory=F('collection__id'))

    queryset = Product.objects.order_by('-unit_price')
    product = Product.objects.earliest('unit_price')
    product = Product.objects.latest('unit_price')

    queryset = Product.objects.all()[5:10]

    queryset = Product.objects.values('id', 'title', 'collection__title')

    queryset = Product.objects.filter(id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')

    queryset = Product.objects.only('id', 'title', 'collection__title')

    queryset = Product.objects.select_related('collection').all()
    queryset = Product.objects.prefetch_related('promotions').all()

    queryset = Order.objects.select_related('customer').order_by('-placed_at')[:5].prefetch_related('orderitem_set__product')

    return render(request, 'hello.html', {'name': 'Mosh', 'orders': queryset})
