from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def item_num(request, num):
    return HttpResponse(num)
