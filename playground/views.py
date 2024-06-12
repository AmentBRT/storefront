from django.shortcuts import render
from store.models import Collection


def say_hello(request):
    collection = Collection.objects.create(title='Video Game', featured_product_id=1)

    return render(request, 'hello.html', {'name': 'Mosh', 'collection': collection})
