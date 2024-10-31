import django.db.models

__all__ = []


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )
    name = django.db.models.TextField(
        max_length=150,
        verbose_name="название",
        help_text="Напишите название товара",
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class AbstractImage(django.db.models.Model):
    image = django.db.models.ImageField(
        "изображение",
        upload_to="catalog/",
    )

    class Meta:
        abstract = True
