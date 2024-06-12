from django.shortcuts import render
from django.db import connection
from store.models import Product


def say_hello(request):
    queryset = Product.objects.raw('SELECT id, title FROM store_product')

    with connection.cursor() as cursor:
        cursor.execute('SELECT id, title, unit_price FROM store_product')
        # cursor.callproc('get_customers', [1, 2, 'a'])

    return render(request, 'hello.html', {'name': 'Mosh', 'queryset': list(queryset)})
