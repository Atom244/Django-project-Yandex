from django.http import HttpResponse
import django.shortcuts
from django.shortcuts import render

import catalog.models

__all__ = ["item_list", "item_detail", "item_num"]


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("name")
    context = {
        "items": items,
    }
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    items = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects.published(),
        pk=pk,
    )
    context = {"item": items}
    return render(request, template, context)


def item_num(request, num):
    return HttpResponse(num)
