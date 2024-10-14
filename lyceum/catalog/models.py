import itertools
import re

import django.core.exceptions
import django.core.validators
import django.db.models

from core.models import AbstractModel


def generate_permutations(word):
    return set("".join(p) for p in itertools.permutations(word, len(word)))


PERMUTATIONS = generate_permutations("превосходно").union(
    generate_permutations("роскошно"),
)


def custom_validator(value):
    pattern = r"\b(превосходно|роскошно)\b"

    if re.search(pattern, value, re.IGNORECASE):
        return

    value_lower = value.lower()
    for word in PERMUTATIONS:
        if word in value_lower:
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
