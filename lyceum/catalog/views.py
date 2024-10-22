from django.http import HttpResponse
from django.shortcuts import render

__all__ = ["item_list", "item_detail", "item_num"]


def item_list(request):
    template = "catalog/item_list.html"
    context = {}
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/includes/item.html"
    context = {"pk": pk}
    return render(request, template, context)


def item_num(request, num):
    return HttpResponse(num)
