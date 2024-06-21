from django.shortcuts import render
from django.http.response import HttpResponse


def product_list(request):
    return HttpResponse('ok')
