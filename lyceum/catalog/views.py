import datetime

import django.db.models
from django.http import HttpResponse
import django.shortcuts
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

import catalog.models


__all__ = []


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.published().order_by("name")
    title = _("Каталог")
    context = {
        "items": items,
        "title": title,
    }
    return render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = catalog.models.Item.objects.published()
    if not item:
        return HttpResponse("Товар отсутствует", status=200)
    items = django.shortcuts.get_object_or_404(
        item,
        pk=pk,
    )
    context = {"item": items}
    return render(request, template, context)


def catalog_new(request):
    template = "catalog/item_list.html"
    end_date = django.utils.timezone.now()
    start_date = end_date - datetime.timedelta(days=7)
    items = (
        catalog.models.Item.objects.published()
        .filter(
            created_at__range=[
                start_date,
                end_date,
            ],
        )
        .order_by("?")
    )[:5]
    title = _("Новинки")
    context = {
        "items": items,
        "title": title,
    }
    return django.shortcuts.render(request, template, context)


def catalog_changed_on_friday(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.published().filter(
            updated_at__week_day=6,
        )
    )[:5]
    title = _("Пятница")
    context = {
        "items": items,
        "title": title,
    }
    return django.shortcuts.render(request, template, context)


def catalog_unverified(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.published()
        .annotate(
            time_diff=django.db.models.ExpressionWrapper(
                django.db.models.F("updated_at")
                - django.db.models.F(
                    "created_at",
                ),
                output_field=django.db.models.DurationField(),
            ),
        )
        .filter(
            time_diff__lte=datetime.timedelta(seconds=1),
        )
    )
    title = _("Непроверенное")
    context = {
        "items": items,
        "title": title,
    }
    return django.shortcuts.render(request, template, context)
