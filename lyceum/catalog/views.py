import datetime

from django.db.models import DurationField, ExpressionWrapper, F
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from catalog.models import Item

__all__ = []


class ItemListView(ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    title = _("Каталог")

    def get_queryset(self):
        return Item.objects.published().order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class ItemDetailView(DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"

    def get_queryset(self):
        return Item.objects.published()

    def get_object(self, queryset=None):
        queryset = self.get_queryset() if queryset is None else queryset
        return get_object_or_404(queryset, pk=self.kwargs["pk"])


class CatalogNewView(ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    title = _("Новинки")

    def get_queryset(self):
        end_date = now()
        start_date = end_date - datetime.timedelta(days=7)
        return (
            Item.objects.published()
            .filter(created_at__range=[start_date, end_date])
            .order_by("?")[:5]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class CatalogChangedOnFridayView(ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    title = _("Пятница")

    def get_queryset(self):
        return Item.objects.published().filter(updated_at__week_day=6)[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context


class CatalogUnverifiedView(ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"
    title = _("Непроверенное")

    def get_queryset(self):
        return (
            Item.objects.published()
            .annotate(
                time_diff=ExpressionWrapper(
                    F("updated_at") - F("created_at"),
                    output_field=DurationField(),
                ),
            )
            .filter(time_diff__lte=datetime.timedelta(seconds=1))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        return context
