import datetime

from django.db.models import Avg
from django.db.models import DurationField, ExpressionWrapper, F
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from catalog.models import Item
from rating.models import Rating


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object

        user_rating = None
        if self.request.user.is_authenticated:
            user_rating = Rating.objects.filter(
                user=self.request.user,
                item=item,
            ).first()

        ratings = Rating.objects.filter(item=item)
        average_rating = ratings.aggregate(avg_score=Avg("score"))["avg_score"]
        total_ratings = ratings.count()

        context.update(
            {
                "user_rating": user_rating,
                "average_rating": average_rating,
                "total_ratings": total_ratings,
            },
        )
        return context

    def post(self, request, *args, **kwargs):
        item = self.get_object()
        score = request.POST.get("score")
        user_rating = Rating.objects.filter(
            user=self.request.user,
            item=item,
        ).first()
        if "delete" in request.POST and user_rating is not None:
            user_rating.delete()
            return redirect("catalog:item-detail", pk=item.pk)

        if score and score.isdigit() and 1 <= int(score) <= 5:
            Rating.objects.update_or_create(
                user=request.user,
                item=item,
                defaults={"score": int(score)},
            )

        return redirect("catalog:item-detail", pk=item.pk)


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
