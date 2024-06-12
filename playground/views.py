from django.shortcuts import render
from store.models import Collection


def say_hello(request):
    collection = Collection(pk=11)
    collection.delete()

    Collection.objects.filter(pk__ft=5).delete()

    return render(request, 'hello.html', {'name': 'Mosh', 'collection': collection})
