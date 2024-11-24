from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Max, Min, Prefetch
from django.views.generic import ListView, TemplateView

from catalog.models import Item
from rating.models import Rating


__all__ = []


class UserStatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "stats/user_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        ratings = Rating.objects.filter(user=user).select_related("item")

        rating_data = ratings.aggregate(
            avg_score=Avg("score"),
            max_score=Max("score"),
            min_score=Min("score"),
        )

        best_rating = ratings.filter(score=rating_data["max_score"]).first()
        worst_rating = ratings.filter(score=rating_data["min_score"]).first()

        best_item = best_rating.item if best_rating else None
        worst_item = worst_rating.item if worst_rating else None

        total_ratings = ratings.count()

        context.update(
            {
                "user": user,
                "best_item": best_item,
                "worst_item": worst_item,
                "average_rating": (
                    round(rating_data["avg_score"], 2)
                    if rating_data["avg_score"]
                    else None
                ),
                "total_ratings": total_ratings,
            },
        )
        return context


class ItemStatisticsView(TemplateView):
    template_name = "stats/item_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = Item.objects.annotate(
            avg_rating=Avg("ratings__score"),
            rating_count=Count("ratings"),
            last_max_rating=Max("ratings__score"),
            last_min_rating=Min("ratings__score"),
        ).prefetch_related(
            Prefetch(
                "ratings",
                queryset=Rating.objects.select_related("user").order_by("-id"),
            ),
        )

        item_stats = []
        for item in items:
            ratings = list(item.ratings.all())
            last_max_rating = next(
                (r for r in ratings if r.score == item.last_max_rating),
                None,
            )
            last_min_rating = next(
                (r for r in ratings if r.score == item.last_min_rating),
                None,
            )

            item_stats.append(
                {
                    "item": item,
                    "avg_rating": round(item.avg_rating, 2),
                    "rating_count": item.rating_count,
                    "last_max_user": (
                        last_max_rating.user if last_max_rating else None
                    ),
                    "last_min_user": (
                        last_min_rating.user if last_min_rating else None
                    ),
                },
            )

        context["item_stats"] = item_stats
        return context


class UserRatedItemsView(LoginRequiredMixin, ListView):
    model = Rating
    template_name = "stats/user_rated_items.html"
    context_object_name = "ratings"

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).order_by(
            "-score",
        )
