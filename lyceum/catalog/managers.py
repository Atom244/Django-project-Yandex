import django.db.models

import catalog.models

__all__ = []


class ItemManager(django.db.models.Manager):
    def published(self):
        queryset = self.get_queryset()
        published_items = self._filter_published(queryset)
        published_items = self._select_related(published_items)
        published_items = self._prefetch_related(published_items)

        return published_items.only(
            "name",
            "text",
            "category__name",
            "main_image__image",
        )

    def _filter_published(self, queryset):
        return queryset.filter(is_published=True, category__is_published=True)

    def _select_related(self, queryset):
        return queryset.select_related("category", "main_image")

    def _prefetch_related(self, queryset):
        return queryset.prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.published().defer(
                    "is_published",
                ),
            ),
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")


class PublishedTagManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)
