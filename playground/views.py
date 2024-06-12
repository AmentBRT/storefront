from django.shortcuts import render
from store.models import Product
from tags.models import TaggedItem


def say_hello(request):
    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    return render(request, 'hello.html', {'name': 'Mosh', 'tags': list(queryset)})
