# import re
from collections import Counter

import django.core.exceptions
import django.core.validators
import django.db.models


from core.models import AbstractModel


def custom_validator(value):
    """pattern = r"\b(превосходно|роскошно)\b"

    if re.search(pattern, value, re.IGNORECASE):
        pass"""

    def contains_word(word, value):
        return not (Counter(word.lower()) - Counter(value.lower()))

    if contains_word("превосходно", value) or contains_word("роскошно", value):
        pass
    else:
        raise django.core.exceptions.ValidationError(
            "В тексте должно быть слово 'превосходно' или 'роскошно'.",
        )


class Tag(AbstractModel):
    slug = django.db.models.TextField(
        verbose_name="Слаг",
        help_text="Напишите слаг",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Category(AbstractModel):
    slug = django.db.models.TextField(
        verbose_name="Слаг",
        help_text="Напишите слаг",
        max_length=200,
        unique=True,
    )
    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name="Вес",
        default=100,
        help_text="Напишите вес товара",
        validators=[
            django.core.validators.MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Item(AbstractModel):
    text = django.db.models.TextField(
        verbose_name="Текст",
        help_text="Напишите описание товара",
        validators=[
            custom_validator,
        ],
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        null=True,
        verbose_name="Категория",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        verbose_name="Теги",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
