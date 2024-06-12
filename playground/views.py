from django.shortcuts import render
from django.db.models  import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Min
from store.models import Product, Customer


def say_hello(request):
    result = Product.objects.aggregate(count=Count('id'), min_price=Min('unit_price'))

    result = Product.objects.annotate(is_new=Value(True))
    result = Customer.objects.annotate(new_id=F('id') + 1)

    result = Customer.objects.annotate(full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT'))
    result = Customer.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

    result = Customer.objects.annotate(orders_count=Count('order'))

    discounted_price = ExpressionWrapper(F('unit_price') * 0.8, DecimalField())
    result = Product.objects.annotate(discounted_price=discounted_price)

    return render(request, 'hello.html', {'name': 'Mosh', 'result': result})
