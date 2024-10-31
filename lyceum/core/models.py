import re

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


class AbstractModelNormalizedName(django.db.models.Model):
    normalized_name = django.db.models.CharField(
        "нормализованное имя",
        max_length=150,
        editable=False,
        null=True,
    )

    def clean(self):
        normalized_name = self._normalize_name(self.name)

        if (
            type(self)
            .objects.exclude(pk=self.pk)
            .filter(normalized_name=normalized_name)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Название, похожее на это уже существует",
            )

        self.normalized_name = normalized_name

    def _normalize_name(self, name):
        similar_letters = {
            "а": "a",
            "в": "b",
            "е": "e",
            "к": "k",
            "м": "m",
            "н": "h",
            "о": "o",
            "р": "p",
            "с": "c",
            "т": "t",
            "у": "y",
            "х": "x",
        }

        normalized = list(re.sub(r"\s+|[^\w\s]", "", name).lower())

        for i in range(len(normalized)):
            if normalized[i] in similar_letters:
                normalized[i] = similar_letters[normalized[i]]

        return "".join(normalized)

    class Meta:
        abstract = True
