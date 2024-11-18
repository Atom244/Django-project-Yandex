from django.contrib import admin

from rating.models import Rating

__all__ = []


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "user", "score")
    list_filter = ("score",)
    search_fields = ("item__name", "user__username")
    raw_id_fields = ("user", "item")
