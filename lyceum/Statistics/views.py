from django.db.models import Avg, Count, Max, Min
from django.views.generic import ListView, TemplateView

from catalog.models import Item
from rating.models import Rating


__all__ = []


class UserStatisticsView(TemplateView):
    template_name = "statistics/user_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        ratings = Rating.objects.filter(user=user)

        best_rating = ratings.order_by("-score").first()
        worst_rating = ratings.order_by("score").first()

        if best_rating:
            best_item = best_rating.item

        if worst_rating:
            worst_item = worst_rating.item

        average_rating = ratings.aggregate(Avg("score"))["score__avg"]
        total_ratings = ratings.count()

        context.update(
            {
                "user": user,
                "best_item": best_item,
                "worst_item": worst_item,
                "average_rating": average_rating,
                "total_ratings": total_ratings,
            },
        )

        return context


class ItemStatisticsView(TemplateView):
    template_name = "statistics/item_statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Аннотируем товары для вычисления агрегированных данных
        items = Item.objects.annotate(
            avg_rating=Avg("ratings__score"),
            rating_count=Count("ratings"),
            last_max_rating=Max("ratings__score"),
            last_min_rating=Min("ratings__score"),
        )

        item_stats = []
        for item in items:
            # Находим пользователей с максимальной и минимальной оценкой
            ratings = Rating.objects.filter(item=item)
            last_max_rating = ratings.filter(score=item.last_max_rating).last()
            last_min_rating = ratings.filter(score=item.last_min_rating).last()

            item_stats.append(
                {
                    "item": item,
                    "avg_rating": item.avg_rating,
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


class UserRatedItemsView(ListView):
    model = Rating
    template_name = "statistics/user_rated_items.html"
    context_object_name = "ratings"

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).order_by(
            "-score",
        )
