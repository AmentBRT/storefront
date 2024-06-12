from django.shortcuts import render
from django.db import transaction
from store.models import Order, OrderItem


def say_hello(request):
    with transaction.atomic():
        order = Order.objects.create(customer_id=1)

        order_item = OrderItem.objects.create(order=order, product_id=1, quantity=1, unit_price=10)

    return render(request, 'hello.html', {'name': 'Mosh', 'order': order})
