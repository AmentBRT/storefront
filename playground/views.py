from django.shortcuts import render
from store.models import Collection


def say_hello(request):
    collection = Collection(pk=11)
    collection.title = 'Games'
    collection.featured_product = None
    collection.save()

    collection = Collection.objects.filter(pk=11).update(featured_product=None)

    return render(request, 'hello.html', {'name': 'Mosh', 'collection': collection})
