import re

import django.core.exceptions
import django.core.validators
import django.db.models

from core.models import AbstractModel


def custom_validator(value):
    patterns = [
        r"[^\w]*р+[^а-яё]*о+[^а-яё]*с+[^а-яё]*к+[^а-яё]*о+"
        r"[^а-яё]*ш+[^а-яё]*н+[^а-яё]*о+[^\w]*",
        r"[^\w]*п+[^а-яё]*р+[^а-яё]*е+[^а-яё]*в+[^а-яё]*о+"
        r"[^а-яё]*с+[^а-яё]*х+[^а-яё]*о+[^а-яё]*д+[^а-яё]*н+[^а-яё]*о+[^\w]*",
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
