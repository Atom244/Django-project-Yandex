import django.db.models

import catalog.models


class ItemManager(django.db.models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True, category__is_published=True)
            .select_related("category", "main_image")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.published().defer(
                        "is_published",
                    ),
                ),
            )
            .only(
                "name",
                "text",
                "category__name",
                "main_image__image",
            )
        )

    def on_main(self):
        return self.published().filter(is_on_main=True).order_by("name")


class PublishedTagManager(django.db.models.Manager):
    def published(self):
        return self.get_queryset().filter(is_published=True)
