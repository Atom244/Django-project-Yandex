import re

import django.core.exceptions
import django.core.validators
import django.db.models

from core.models import AbstractModel


def custom_validator(value):
    patterns = [
        r"(?:^|\W|\d)роскошно(?:\W|\d|$)",
        r"(?:^|\W|\d)превосходно(?:\W|\d|$)",
    ]

    for pattern in patterns:
        if re.search(pattern, value, re.IGNORECASE):
            return

    raise django.core.exceptions.ValidationError(
        "В тексте должно быть слово 'превосходно' или 'роскошно'.",
    )


class Tag(AbstractModel):
    slug = django.db.models.TextField(
        verbose_name="слаг",
        help_text="Напишите слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.TextField(
        verbose_name="слаг",
        help_text="Напишите слаг",
        max_length=200,
        unique=True,
    )
    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name="вес",
        default=100,
        help_text="Напишите вес товара",
        validators=[
            django.core.validators.MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(AbstractModel):
    text = django.db.models.TextField(
        verbose_name="текст",
        help_text="Напишите описание товара",
        validators=[
            custom_validator,
        ],
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        null=True,
        verbose_name="категория",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="теги",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
